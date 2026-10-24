from __future__ import annotations

import json
import io
from contextlib import redirect_stderr, redirect_stdout
from http.client import IncompleteRead
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from test_helpers import REPO_ROOT, load_module

fetch = load_module("fetch", REPO_ROOT / "skills/pixellab-pip/assets/fetch.py")
manifest = load_module("manifest", REPO_ROOT / "skills/pixellab-pip/assets/manifest.py")
def image_bytes(color=(20, 40, 60, 255), fmt="PNG"):
    buf = io.BytesIO()
    Image.new("RGBA", (2, 2), color).save(buf, format=fmt)
    return buf.getvalue()


PNG = image_bytes()
LINK = "https://backblaze.pixellab.ai/file/result.png"


def links(n):
    return [LINK + str(i) for i in range(n)]


class FetchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.original_get = fetch.get

    def tearDown(self) -> None:
        fetch.get = self.original_get
        self.tmp.cleanup()

    def test_frames_saved_in_order(self) -> None:
        fetch.get = lambda url, **kwargs: ("ok", image_bytes((int(url[-1]), 40, 60, 255)))
        self.assertEqual(fetch.try_job(links(3), str(self.root / "clip")), "ok")
        self.assertEqual([p.name for p in sorted((self.root / "clip").iterdir())], ["0.png", "1.png", "2.png"])
        with Image.open(self.root / "clip" / "2.png") as image:
            self.assertEqual(image.getpixel((0, 0))[0], 2)

    def test_missing_later_frame_never_proves_shorter_clip_complete(self) -> None:
        fetch.get = lambda url, **kwargs: ("ok", PNG) if int(url[-1]) < 3 else ("wait", None)
        self.assertEqual(fetch.try_job(links(5), str(self.root / "clip")), "wait")
        self.assertFalse((self.root / "clip").exists())

    def test_file_errors_never_prove_failure_or_refund(self) -> None:
        import urllib.error
        for code, status in ((404, "wait"), (429, "wait"), (503, "wait"), (410, "unavailable"),
                             (403, "unavailable"), (400, "unavailable"), (422, "unavailable")):
            error = urllib.error.HTTPError("https://api.pixellab.ai/", code, "file unavailable", {}, None)
            with patch.object(fetch, "_download", side_effect=error):
                self.assertEqual(fetch.get(LINK), (status, None))

    def test_truncated_http_body_keeps_reservation_and_directs_recovery(self) -> None:
        class Resp:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, n=-1): raise IncompleteRead(b"partial", 100)

        for direct in (False, True):
            with self.subTest(direct=direct):
                run = self.root / ("direct" if direct else "job")
                out = run / "raw.png"
                args = ["--url", "https://backblaze.pixellab.ai/file/result.png", str(out)] if direct else [
                    "job-truncated", str(out), "--run", str(run), "--url", LINK, "--estimate", "7", "--timeout", "1"]
                output = io.StringIO()
                with patch.object(fetch.OPENER, "open", return_value=Resp()) as download, \
                        patch.object(fetch, "time") as clock, redirect_stdout(output):
                    clock.monotonic.side_effect = [0, 0, 1]
                    self.assertEqual(fetch.main(args), 3)
                download.assert_called_once()
                self.assertIn("matching getter", output.getvalue())
                self.assertIn("do not resubmit", output.getvalue())
                self.assertFalse(out.exists())
                if not direct:
                    self.assertEqual(manifest.committed(str(run)), 7)
                    self.assertEqual(manifest.jobs(str(run))[0]["job_id"], "job-truncated")
                    self.assertEqual(manifest.jobs(str(run))[0]["status"], "submitted")
                    self.assertEqual(manifest.jobs(str(run))[0]["download_status"], "wait")

    def test_blocked_result_keeps_credit_reservation_and_explains_recovery(self) -> None:
        run = self.root / "blocked"
        out = run / "raw.png"
        stderr = io.StringIO()
        with patch.object(fetch, "_download", return_value=b"<html>login required</html>"), redirect_stderr(stderr):
            self.assertEqual(fetch.main(["job-html", str(out), "--run", str(run), "--url", LINK, "--estimate", "7"]), 2)
        self.assertIn("matching getter", stderr.getvalue())
        self.assertIn("saved outputs", stderr.getvalue())
        self.assertIn("do not resubmit or infer a refund", stderr.getvalue())
        self.assertFalse(out.exists())
        self.assertEqual(manifest.committed(str(run)), 7)
        self.assertEqual(manifest.jobs(str(run))[0]["status"], "submitted")

    def test_writes_manifest_entry(self) -> None:
        fetch.get = lambda url, **kwargs: ("ok", PNG)
        run = self.root / "run"
        rc = fetch.main(["job-1", str(run / "keys" / "A.png"), "--run", str(run), "--url", LINK,
                         "--tool", "MCP edit_image_pro_flash",
                         "--generations", "6", "--timeout", "1"])
        self.assertEqual(rc, 0)
        entry = manifest.jobs(str(run))[0]
        self.assertEqual((entry["job_id"], entry["status"], entry["reported_usage"]), ("job-1", "ok", {"generations": 6.0}))
        self.assertEqual(entry["outputs"], ["keys/A.png"])

    def test_oversized_download_bomb_or_image_named_clip_writes_nothing(self) -> None:
        class Resp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n=-1): return b"x" * n

        with patch.object(fetch.OPENER, "open", return_value=Resp()), patch.object(fetch, "MAX_BYTES", 10):
            with self.assertRaisesRegex(ValueError, "exceeds"):
                fetch._download(LINK)
        with patch.object(Image, "MAX_IMAGE_PIXELS", 2), self.assertRaises(ValueError):
            fetch.validate_image(PNG)
        fetch.get = lambda *args, **kwargs: self.fail("image-named clip reached HTTP")
        with self.assertRaises(ValueError):
            fetch.try_job(links(2), str(self.root / "clip.png"))
        self.assertFalse((self.root / "clip.png").exists())

    def test_failed_write_leaves_no_partial_output(self) -> None:
        fetch.get = lambda url, **kwargs: ("ok", PNG)
        real_open = Path.open

        def flaky_open(self, *args, **kwargs):
            if self.name == "1.png":
                raise OSError(28, "No space left on device")
            return real_open(self, *args, **kwargs)

        clip = self.root / "clip"
        with patch.object(Path, "open", flaky_open), self.assertRaises(OSError):
            fetch.try_job(links(3), str(clip))
        self.assertFalse(clip.exists())  # 0.png and the folder were removed, so a retry works
        self.assertEqual(fetch.try_job(links(3), str(clip)), "ok")

    def test_redirects_and_plain_http_stay_on_pixellab(self) -> None:
        # review: only the first URL was checked; a redirect could leave PixelLab, and http was accepted
        with self.assertRaises(ValueError):
            fetch.check_host("http://backblaze.pixellab.ai/file/x.png")
        guard = fetch.PixelLabOnly()
        with self.assertRaises(ValueError):
            guard.redirect_request(None, None, 302, "Found", {}, "https://example.com/x.png")

    def test_url_refuses_an_existing_file(self) -> None:
        # review: --url wrote over an existing path, raw PixelLab files included
        out = self.root / "raw.png"
        out.write_bytes(PNG)
        self.assertEqual(fetch.main(["--url", "https://backblaze.pixellab.ai/file/x.png", str(out)]), 2)

    def test_url_download_sends_a_user_agent(self) -> None:
        # e2e run 3: rotation links on PixelLab's file host refused Python's default user agent (403)
        seen = {}

        class Resp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n=-1): return PNG

        original = fetch.OPENER.open
        def fake(req, timeout=30):
            seen["ua"] = req.get_header("User-agent")
            return Resp()
        fetch.OPENER.open = fake
        try:
            out = self.root / "rot" / "south.png"
            self.assertEqual(fetch.main(["--url", "https://backblaze.pixellab.ai/file/x/south.png", str(out)]), 0)
        finally:
            fetch.OPENER.open = original
        self.assertTrue(out.exists())
        self.assertTrue(seen["ua"] and "Python-urllib" not in seen["ua"])
        self.assertEqual(fetch.main(["--url", "https://example.com/x.png", str(out)]), 2)

    def test_rejects_non_pixellab_host(self) -> None:
        with self.assertRaises(ValueError):
            fetch.check_host("https://example.com/x.png")
        fetch.check_host(LINK)
        run = self.root / "run"
        fetch.get = lambda *args, **kwargs: self.fail("unlisted host reached HTTP")
        self.assertEqual(fetch.main(["j", str(run / "raw.png"), "--run", str(run), "--url", "https://example.com/x.png"]), 2)
        self.assertFalse(run.exists())

    def test_corrupt_or_wrong_format_result_writes_nothing(self) -> None:
        for data in (b"<html>login</html>", PNG[:12], image_bytes(fmt="GIF")):
            fetch.get = lambda url, **kwargs: ("ok", data)
            with self.assertRaises(ValueError):
                fetch.try_job([LINK], str(self.root / "raw.png"))
            self.assertFalse((self.root / "raw.png").exists())
        with patch.object(fetch, "_download", return_value=b"<html>bad</html>"):
            self.assertEqual(fetch.main(["--url", "https://backblaze.pixellab.ai/file/x.png",
                                         str(self.root / "raw.png")]), 2)
        self.assertFalse((self.root / "raw.png").exists())

    def test_existing_outputs_never_overwritten_or_mixed(self) -> None:
        clip = self.root / "clip"
        clip.mkdir()
        (clip / "1.png").write_bytes(PNG)
        fetch.get = lambda *args: self.fail("existing destination reached HTTP")
        with self.assertRaises(ValueError):
            fetch.try_job(links(2), str(clip))
        self.assertEqual(list(clip.iterdir()), [clip / "1.png"])
        raw = self.root / "raw.png"
        raw.write_bytes(PNG)
        with self.assertRaises(ValueError):
            fetch.try_job([LINK], str(raw))
        self.assertEqual(raw.read_bytes(), PNG)

    def test_exact_outputs_and_repeat_fetch_preserve_raw_bytes(self) -> None:
        run = self.root / "run"
        fetch.get = lambda url, **kwargs: ("ok", PNG)
        args = ["j", str(run / "frames"), "--run", str(run), "--url", LINK + "0", "--url", LINK + "1",
                "--estimate", "7", "--timeout", "1"]
        self.assertEqual(fetch.main(args), 0)
        entry = manifest.jobs(str(run))[0]
        self.assertEqual(entry["outputs"], ["frames/0.png", "frames/1.png"])
        self.assertNotIn("reported_usage", entry)
        self.assertEqual(entry["estimated_usage"], {"generations": 7})
        self.assertEqual(fetch.main(args), 2)  # safe refusal, no assumption of same-job identity
        self.assertEqual((run / "frames" / "0.png").read_bytes(), PNG)

    def test_pending_and_unavailable_downloads_keep_reservations(self) -> None:
        for status, code in (("wait", 3), ("unavailable", 2)):
            run = self.root / status
            fetch.get = lambda url, **kwargs: (status, None)
            args = ["j", str(run / "raw.png"), "--run", str(run), "--url", LINK, "--estimate", "6", "--timeout", "0.02"]
            self.assertEqual(fetch.main(args), code)
            self.assertEqual(manifest.committed(str(run)), 6)
            self.assertEqual(manifest.jobs(str(run))[0]["status"], "submitted")
            self.assertFalse((run / "raw.png").exists())

    def test_refetch_to_new_destination_retains_all_output_provenance(self) -> None:
        run = self.root / "run"
        fetch.get = lambda url, **kwargs: ("ok", PNG)
        for name in ("raw.png", "copy.png"):
            self.assertEqual(fetch.main(["j", str(run / name), "--run", str(run), "--url", LINK, "--generations", "6"]), 0)
        entry = manifest.jobs(str(run))[0]
        self.assertEqual(entry["outputs"], ["raw.png", "copy.png"])
        fetch.get = lambda url, **kwargs: ("unavailable", None)
        self.assertEqual(fetch.main(["j", str(run / "later.png"), "--run", str(run), "--url", LINK]), 2)
        self.assertEqual(manifest.jobs(str(run))[0]["status"], "ok")
        self.assertEqual(manifest.spent(str(run)), 6)

    def test_invalid_arguments_and_ledger_fail_before_http(self) -> None:
        run = self.root / "run"
        run.mkdir()
        path = run / "manifest.json"
        path.write_text('{"calls": []}', encoding="utf-8")
        fetch.get = lambda *args: self.fail("invalid preflight reached HTTP")
        args = ["j", str(run / "raw.png"), "--run", str(run), "--url", LINK]
        self.assertEqual(fetch.main(args), 2)
        self.assertEqual(path.read_text(encoding="utf-8"), '{"calls": []}')
        self.assertEqual(fetch.main([*args, "--estimate", "nan"]), 2)
        self.assertEqual(fetch.main(["j", str(self.root / "outside.png"), "--run", str(run), "--url", LINK]), 2)

    def test_missing_pillow_skips_before_network_or_writes(self) -> None:
        script = REPO_ROOT / "skills/pixellab-pip/assets/fetch.py"
        code = (f"import runpy,sys; sys.path.insert(0,{str(script.parent)!r}); sys.modules['PIL']=None; "
                f"sys.argv=['fetch.py','j','raw.png','--run','run','--url',{LINK!r}]; runpy.run_path({str(script)!r},run_name='__main__')")
        result = subprocess.run([sys.executable, "-c", code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "skipped")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_deadline_bounds_each_frame_and_writes_no_partial_clip(self) -> None:
        calls = []
        def fake(url, **kwargs):
            calls.append(kwargs["timeout"])
            return "ok", PNG
        fetch.get = fake
        with patch.object(fetch.time, "monotonic", side_effect=[10, 12]):
            status = fetch.try_job(links(2), str(self.root / "clip"), deadline=11)
        self.assertEqual(status, "wait")
        self.assertEqual(calls, [1])
        self.assertFalse((self.root / "clip").exists())


if __name__ == "__main__":
    unittest.main()
