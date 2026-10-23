from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_helpers import REPO_ROOT, load_module

fetch = load_module("fetch", REPO_ROOT / "skills/pixellab-pip/assets/fetch.py")
manifest = load_module("manifest", REPO_ROOT / "skills/pixellab-pip/assets/manifest.py")
PNG = b"\x89PNG\r\n\x1a\n" + b"x" * 8


class FetchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.original_get = fetch.get

    def tearDown(self) -> None:
        fetch.get = self.original_get
        self.tmp.cleanup()

    def test_frames_saved_in_order(self) -> None:
        fetch.get = lambda job, index=None: ("ok", PNG + bytes([index]))
        self.assertEqual(fetch.try_job("j", str(self.root / "clip"), 3), "ok")
        self.assertEqual([p.name for p in sorted((self.root / "clip").iterdir())], ["0.png", "1.png", "2.png"])
        self.assertEqual((self.root / "clip" / "2.png").read_bytes()[-1], 2)

    def test_short_clip_takes_frames_it_has(self) -> None:
        fetch.get = lambda job, index=None: ("ok", PNG) if index < 3 else ("notfound", None)
        self.assertEqual(fetch.try_job("j", str(self.root / "clip"), 5), "ok")
        self.assertEqual(len(list((self.root / "clip").iterdir())), 3)

    def test_404_grace_then_failed(self) -> None:
        self.assertEqual(fetch.settle("notfound", 5), "wait")
        self.assertEqual(fetch.settle("notfound", 200), "failed")
        self.assertEqual(fetch.settle("ok", 999), "ok")

    def test_writes_manifest_entry(self) -> None:
        fetch.get = lambda job, index=None: ("ok", PNG)
        run = self.root / "run"
        rc = fetch.main(["job-1", str(run / "keys" / "A.png"), "--run", str(run), "--tool", "MCP edit_image_pro_flash",
                         "--generations", "6", "--timeout", "0"])
        self.assertEqual(rc, 0)
        entry = manifest.jobs(str(run))[0]
        self.assertEqual((entry["job_id"], entry["status"], entry["reported_usage"]), ("job-1", "ok", {"generations": 6.0}))
        self.assertEqual(entry["outputs"], ["keys/A.png"])

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
            def read(self): return PNG

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
        with self.assertRaises(ValueError):
            fetch.main(["--url", "https://example.com/x.png", str(out)])

    def test_rejects_non_pixellab_host(self) -> None:
        with self.assertRaises(ValueError):
            fetch.check_host("https://example.com/x.png")
        fetch.check_host(fetch.BASE % "abc")


if __name__ == "__main__":
    unittest.main()
