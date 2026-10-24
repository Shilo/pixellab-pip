from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


from test_helpers import REPO_ROOT, load_module

FINISH = REPO_ROOT / "skills/pixellab-pip/assets/finish"


try:
    import numpy as np
    import scipy.ndimage  # noqa: F401
    from PIL import Image
    synth = load_module("synth", REPO_ROOT / "tests/doctor_cases/synth.py")
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

CLEANUP = ["scrub", "despeckle", "ground_snap", "colormatch", "recolor_trail", "recolor_groups", "recolor_like",
           "apply_palette", "dir8_finish"]
NEW_PIXELS = ["slash_layer", "throw_prop", "bake_fx", "blade_trail"]


def run(helper: str, *args, env=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(FINISH / f"{helper}.py"), *map(str, args)], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env)


def hashes(folder: Path) -> dict:
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


# --- one small fixture per helper: every input lives under <tmp>/in, returns the args without --out ---

def case_scrub(t):
    fs = synth.walk(4)
    fs[1][2:5, 2:8] = (255, 240, 120, 255)                              # a generator flash in no key-pose colour
    for i, f in enumerate(fs):
        synth.png(f, t / "in/raw" / f"{i}.png")
    return [t / "in/raw", "1", "2"]


def case_despeckle(t):
    return [synth.png(synth.figure(), t / "in/0.png")]


def case_ground_snap(t):
    fs = synth.walk(2)
    fs[1] = synth.shift(fs[1], 0, -6)
    return [synth.png(synth.figure(), t / "in/still.png"), "0,0", *synth.save(fs, t / "in/src", "k_attack")]


def case_colormatch(t):
    return [synth.png(synth.figure(), t / "in/still.png"), synth.png(synth.bright(synth.figure(), 1.3), t / "in/f/1.png")]


def _trail_frame(t):
    tab, red = (121, 23, 20), (250, 6, 5)
    still = synth.figure().copy()
    still[30:34, 20:24, :3] = tab                                       # a tabard in the hero's own dark red
    f = still.copy()
    f[22:24, 2:23] = red + (255,)                                       # the streak, running into the body
    f[21, 2:18] = tab + (255,)                                          # its outline, in the hero's colours
    f[24, 2:18] = tab + (255,)
    return still, f


def case_recolor_trail(t):
    still, f = _trail_frame(t)
    synth.png(f, t / "in/raw/0.png")
    return [t / "in/raw", "0", "--hue", "red", "--to", "none", "--ref", synth.png(still, t / "in/still.png")]


def case_recolor_groups(t):
    return [synth.png(synth.figure(), t / "in/still.png"), synth.png(synth.walk(2)[1], t / "in/f/1.png"),
            "--swap", "blue=crimson"]


def case_recolor_like(t):
    new = synth.figure().copy()
    on = (new[..., :3] == synth.BLUE).all(-1)
    new[on, :3] = (170, 60, 60)
    return [synth.png(synth.figure(), t / "in/old.png"), synth.png(new, t / "in/new.png"),
            synth.png(synth.walk(2)[1], t / "in/f/1.png")]


def case_apply_palette(t):
    return ["#000000,#ffffff,#3c5aaa", synth.png(synth.figure(), t / "in/f/1.png")]


def case_dir8_finish(t):
    for i, f in enumerate(synth.walk(3)):
        synth.png(f, t / "in/anim/east" / f"{i}.png")
    sheet = np.zeros((4, 8, 4), np.uint8)
    sheet[1:3, :, :] = (255, 220, 90, 255)
    synth.png(sheet, t / "in/vfx/flash.png")
    spec = {"speck": 4, "flash": {"sheet": "vfx/flash.png", "frame_w": 4, "anchor": [0, 2]},
            "dirs": {"east": {"src": "anim/east", "shot": 1, "muzzle": [40, 20], "angle": 0}},
            "mirror": {"west": "east"}}
    (t / "in/spec.json").write_text(json.dumps(spec), encoding="utf-8")
    return [t / "in/spec.json"]


def case_slash_layer(t):
    raw = synth.figure().copy()
    raw[2:6, 2:12] = (240, 240, 255, 255)
    return ["extract", synth.png(raw, t / "in/3.png"), synth.png(synth.figure(), t / "in/3_s.png")]


def case_throw_prop(t):
    rel = synth.figure().copy()
    rel[2:4, 2:14] = (200, 180, 90, 255)                                # the spear, apart from the body
    after = synth.png(synth.figure(), t / "in/after.png")
    return [synth.png(rel, t / "in/release.png"), "--onto", after, after, "--step", "3,1"]


def _boom(t):
    sheet = Image.new("RGBA", (12, 4))
    for k in range(3):
        sheet.paste((255, 0, 200 + k * 20, 255), (4 * k, 0, 4 * k + 4, 4))
    os.makedirs(t / "in", exist_ok=True)
    sheet.save(t / "in/boom.png")
    (t / "in/boom.json").write_text(json.dumps(
        {"frames": [{"frame": {"x": 4 * k, "y": 0, "w": 4, "h": 4}, "duration": 83} for k in range(3)]}))
    return t / "in/boom.png"


def case_bake_fx(t):
    paths = synth.save(synth.walk(3), t / "in/f", "k_skill")
    return [*paths, "--fx", _boom(t), "--at", "60,10", "--from", "2", "--widen", "70"]


def case_blade_trail(t):
    a, b = synth.save(synth.walk(2), t / "in/f", "k")
    return ["--frames", a, b, "--path", "4,30 30,34 44,20", "--spans", "x,0:1", "--thick", "0,6"]


CASES = {name: globals()[f"case_{name}"] for name in CLEANUP + NEW_PIXELS}


class FinishContractTests(unittest.TestCase):
    def test_finish_skips_without_numpy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "numpy"
            blocker.mkdir()
            (blocker / "__init__.py").write_text('raise ImportError("blocked for the test")\n', encoding="utf-8")
            env = {**os.environ, "PYTHONPATH": tmp + os.pathsep + os.environ.get("PYTHONPATH", ""),
                   "PYTHONDONTWRITEBYTECODE": "1"}
            for name in CASES:
                with self.subTest(helper=name):
                    r = run(name, "x.png", "--out", Path(tmp) / "out", env=env)
                    self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
                    self.assertEqual(json.loads(r.stdout)["status"], "skipped")
                    self.assertIn("numpy", json.loads(r.stdout)["reason"])
                    self.assertFalse((Path(tmp) / "out").exists())

    @unittest.skipUnless(HAS_NUMPY, "numpy/scipy not installed")
    def test_finish_skips_when_pillow_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "PIL"
            blocker.mkdir()
            (blocker / "__init__.py").write_text('raise ImportError("Pillow blocked for the test")')
            env = {**os.environ, "PYTHONPATH": tmp + os.pathsep + os.environ.get("PYTHONPATH", "")}
            result = run("colormatch", "still.png", "frame.png", "--out", Path(tmp) / "out", env=env)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "skipped")
            self.assertFalse((Path(tmp) / "out").exists())

    @unittest.skipUnless(HAS_NUMPY, "numpy/scipy not installed")
    def test_out_required(self) -> None:
        for name, case in CASES.items():
            with self.subTest(helper=name), tempfile.TemporaryDirectory() as tmp:
                r = run(name, *case(Path(tmp)))
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertIn("--out", r.stderr)

    @unittest.skipUnless(HAS_NUMPY, "numpy/scipy not installed")
    def test_inputs_unchanged_and_derivative_label_written(self) -> None:
        for name, case in CASES.items():
            with self.subTest(helper=name), tempfile.TemporaryDirectory() as tmp:
                t = Path(tmp)
                args = case(t)
                before = hashes(t / "in")
                r = run(name, *args, "--out", t / "out")
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertEqual(hashes(t / "in"), before)              # inputs never modified
                label = json.loads((t / "out/derivative.json").read_text(encoding="utf-8"))
                self.assertEqual(label["helper"], name)
                self.assertEqual(label["category"], "cleanup" if name in CLEANUP else "new_pixels")
                self.assertTrue(label["inputs"] and all(os.path.exists(p) for p in label["inputs"]), label["inputs"])
                self.assertIsInstance(label["changes"], dict)
                self.assertTrue(any(p.suffix == ".png" for p in (t / "out").rglob("*")))

    @unittest.skipUnless(HAS_NUMPY, "numpy/scipy not installed")
    def test_refuses_to_write_over_an_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(case_despeckle(Path(tmp))[0])
            raw = p.read_bytes()
            r = run("despeckle", p, "--out", p.parent)
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual(p.read_bytes(), raw)


@unittest.skipUnless(HAS_NUMPY, "numpy/scipy not installed")
class FinishBehaviourTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.t = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_find_muzzle_locates_the_flash_frame_and_muzzle(self) -> None:
        clip = self.t / "shot"
        clip.mkdir()
        for i in range(4):
            px = np.zeros((40, 40, 4), np.uint8)
            px[10:30, 10:20] = (60, 40, 40, 255)        # body
            px[15, 20:29] = (200, 200, 210, 255)        # light gun barrel ending at x=28
            if i == 2:
                px[12:20, 29:37] = (255, 220, 60, 255)  # the generator's flash at the barrel
            Image.fromarray(px, "RGBA").save(clip / f"{i}.png")
        before = hashes(clip)
        r = run("find_muzzle", clip)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("shot frame 2", r.stdout)
        self.assertIn("muzzle ~(29, 15)", r.stdout)
        self.assertEqual(hashes(clip), before)

    def ok(self, helper, *args):
        r = run(helper, *args)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def img(self, path):
        return np.array(Image.open(path).convert("RGBA"))

    def test_second_run_requires_a_fresh_folder_and_preserves_derivative(self) -> None:
        src = case_despeckle(self.t)[0]
        self.ok("despeckle", src, "--out", self.t / "o")
        before = hashes(self.t / "o")
        self.assertNotEqual(run("despeckle", src, "--out", self.t / "o", "--tol", "60").returncode, 0)
        self.assertEqual(hashes(self.t / "o"), before)

    def test_blade_trail_ghost_alone_draws_on_the_trail_frames(self) -> None:
        # bloat review: the documented `--ghost` call drew nothing without an undocumented --ghost-on
        args = case_blade_trail(self.t)
        self.ok("blade_trail", *args, "--ghost", args[1], "--out", self.t / "o")
        frames = json.loads((self.t / "o/derivative.json").read_text())["changes"]["frames"]
        self.assertEqual((frames["0.png"]["ghost"], frames["1.png"]["ghost"]), (False, True))

    def test_despeckle_removes_lone_pixels_and_keeps_highlights(self) -> None:
        f = synth.figure().copy()
        f[30, 22] = (250, 250, 250, 255)                                # a lone white speck in the blue body
        f[24:26, 20:22] = (250, 250, 250, 255)                          # a 2x2 highlight: real detail, stays
        f[3, 3] = (200, 200, 200, 255)                                  # a floating stray pixel
        self.ok("despeckle", synth.png(f, self.t / "in/0.png"), "--out", self.t / "o")
        o = self.img(self.t / "o/0.png")
        self.assertEqual(tuple(o[30, 22, :3]), synth.BLUE)
        self.assertTrue((o[24:26, 20:22, :3] == 250).all())
        self.assertEqual(o[3, 3, 3], 0)
        label = json.loads((self.t / "o/derivative.json").read_text())
        self.assertEqual(label["changes"]["frames"]["0.png"], {"specks": 3, "strays": 1})   # the speck + the two 1 px eyes

    def test_scrub_clears_a_box_on_one_key_pose(self) -> None:
        f = synth.figure().copy()
        f[12:14, 30:47] = (240, 255, 255, 255)                          # a beam right of the face
        self.ok("scrub", synth.png(f, self.t / "in/pose.png"), "--box", "29,10,47,16", "--out", self.t / "o")
        o = self.img(self.t / "o/pose_s.png")
        self.assertFalse(o[12:14, 31:47, 3].any())
        body = synth.figure()[..., 3] > 0
        body[10:17, 29:48] = False
        self.assertTrue((o[..., 3][body] == 255).all())

    def test_scrub_clears_flash_colours_in_a_raw_clip(self) -> None:
        args = case_scrub(self.t)
        self.ok("scrub", *args, "--out", self.t / "o")
        o = self.img(self.t / "o/1_s.png")
        self.assertFalse(o[2:5, 2:8, 3].any())
        self.assertTrue((o[..., 3] > 0).sum() > 500)

    def test_recolor_trail_delete_takes_the_outline_and_leaves_no_hole(self) -> None:
        still, _ = _trail_frame(self.t)
        self.ok("recolor_trail", *case_recolor_trail(self.t), "--out", self.t / "o")
        o = self.img(self.t / "o/0_t.png")
        self.assertFalse(o[21:25, 2:17, 3].any())                       # streak and outline both gone
        self.assertTrue(o[22:24, 19:23, 3].all())                       # no hole where it crossed the body
        self.assertTrue((o[30:34, 20:24] == still[30:34, 20:24]).all())  # the tabard stays

    def test_ground_snap_out_gets_every_frame_in_a_new_folder(self) -> None:
        args = case_ground_snap(self.t)
        self.ok("ground_snap", *args, "--out", self.t / "new/dir")
        self.assertEqual(sorted(os.listdir(self.t / "new/dir")),
                         sorted(["derivative.json"] + [os.path.basename(p) for p in args[2:]]))
        moved = self.img(self.t / "new/dir" / os.path.basename(args[3]))
        self.assertEqual(int(np.nonzero(moved[..., 3].any(1))[0].max()), 53)   # back on the feet line

    def test_ground_snap_fx_frames_are_left_alone(self) -> None:
        args = case_ground_snap(self.t)
        r = self.ok("ground_snap", *args, "--fx", "2", "--out", self.t / "o")
        self.assertEqual(Image.open(self.t / "o" / os.path.basename(args[3])).tobytes(), Image.open(args[3]).tobytes())
        self.assertIn("fx", r.stdout)

    def test_ground_snap_warns_below_the_feet_line_and_check_writes_nothing(self) -> None:
        fs = synth.walk(2)
        fs[1] = synth.shift(fs[1], 0, 2)
        paths = synth.save(fs, self.t / "in/src", "k")
        r = self.ok("ground_snap", synth.png(synth.figure(), self.t / "in/still.png"), "0,0", *paths, "--check")
        self.assertIn("below the feet line", r.stdout)   # --check needs no --out and writes nothing
        self.assertFalse((self.t / "derivative.json").exists())

    def test_colormatch_snaps_to_the_still_palette(self) -> None:
        still, frame = case_colormatch(self.t)
        self.ok("colormatch", still, frame, "--out", self.t / "o")
        o = self.img(self.t / "o/1.png")
        pal = {tuple(p) for p in self.img(still)[..., :3][self.img(still)[..., 3] > 0]}
        self.assertTrue({tuple(p) for p in o[..., :3][o[..., 3] > 0]} <= pal)

    def test_recolor_groups_moves_a_group_and_keeps_skin(self) -> None:
        still = synth.png(synth.figure(), self.t / "in/still.png")
        self.ok("recolor_groups", still, "--swap", "blue=crimson", "--out", self.t / "o")
        o = self.img(self.t / "o/still.png")
        self.assertGreater(o[30, 20, 0], o[30, 20, 2])                  # the blue coat went red
        self.assertEqual(tuple(o[13, 22, :3]), synth.SKIN)              # skin never moves unless named

    def test_throw_prop_flies_the_detached_weapon(self) -> None:
        self.ok("throw_prop", *case_throw_prop(self.t), "--out", self.t / "o")
        f1, f2 = self.img(self.t / "o/0.png"), self.img(self.t / "o/1.png")
        self.assertTrue((f1[3:5, 5:17] == (200, 180, 90, 255)).all())   # one step
        self.assertTrue((f2[4:6, 8:20] == (200, 180, 90, 255)).all())   # two steps
        body = synth.figure()[..., 3] > 0
        self.assertTrue((f1[body] == synth.figure()[body]).all())

    def test_throw_prop_turns_the_prop(self) -> None:
        rel, _, after = case_throw_prop(self.t)[:3]
        self.ok("throw_prop", rel, "--onto", after, "--step", "0,0", "--turn", "1", "--out", self.t / "o")
        ys, xs = np.nonzero((self.img(self.t / "o/0.png")[..., :3] == (200, 180, 90)).all(-1))
        self.assertGreater(ys.max() - ys.min(), xs.max() - xs.min())

    def test_bake_fx_lays_an_effect_from_a_frame_and_holds_the_body(self) -> None:
        self.ok("bake_fx", *case_bake_fx(self.t), "--out", self.t / "o")
        outs = sorted((self.t / "o").glob("*.png"))
        self.assertEqual(len(outs), 4)                                  # 3 body frames, the last held
        last = self.img(outs[-1])
        self.assertEqual(last.shape[1], 70)
        self.assertEqual(tuple(last[10, 60]), (255, 0, 240, 255))
        self.assertEqual(self.img(outs[0])[10, 60, 3], 0)
        label = json.loads((self.t / "o/derivative.json").read_text())
        self.assertEqual(label["changes"]["held_frames"], 1)

    def test_bake_fx_anchor_lands_on_at(self) -> None:
        paths = synth.save(synth.walk(1), self.t / "in/f", "k")
        sheet = Image.new("RGBA", (20, 10))
        sheet.putpixel((2, 5), (255, 0, 200, 255))
        sheet.save(self.t / "in/beam.png")
        (self.t / "in/beam.json").write_text(json.dumps({"frames": [{"frame": {"x": 0, "y": 0, "w": 20, "h": 10}}]}))
        self.ok("bake_fx", *paths, "--fx", self.t / "in/beam.png", "--at", "30,12", "--anchor", "2,5", "--from", "1",
                "--out", self.t / "o")
        self.assertEqual(tuple(self.img(self.t / "o/0.png")[12, 30]), (255, 0, 200, 255))

    def test_slash_layer_apply_with_offset(self) -> None:
        frame = synth.png(synth.figure(), self.t / "in/3.png")
        fx = np.zeros((synth.H, synth.W, 4), np.uint8)
        fx[2, 2] = (230, 240, 255, 255)
        self.ok("slash_layer", "apply", frame, synth.png(fx, self.t / "in/cres.png"), "--offset", "3,2",
                "--out", self.t / "o")
        o = self.img(self.t / "o/3.png")
        self.assertEqual(tuple(o[4, 5]), (230, 240, 255, 255))
        self.assertEqual(o[2, 2, 3], 0)

    def test_blade_trail_behind_keeps_the_body_on_top(self) -> None:
        body = np.zeros((48, 64, 4), np.uint8)
        body[20:40, 20:40] = (200, 0, 0, 255)
        p = synth.png(body, self.t / "in/b.png")
        common = ["--frames", p, "--path", "4,30 60,30", "--spans", "0:1", "--thick", "6"]
        self.ok("blade_trail", *common, "--out", self.t / "over")
        self.ok("blade_trail", *common, "--behind", "--out", self.t / "under")
        self.assertEqual(tuple(self.img(self.t / "under/0.png")[30, 30, :3]), (200, 0, 0))
        self.assertNotEqual(tuple(self.img(self.t / "over/0.png")[30, 30, :3]), (200, 0, 0))

    def test_dir8_finish_mirrors_and_keeps_the_frame_count(self) -> None:
        self.ok("dir8_finish", *case_dir8_finish(self.t), "--out", self.t / "o")
        self.assertEqual(sorted(os.listdir(self.t / "o/east")), ["0.png", "1.png", "2.png"])
        east = self.img(self.t / "o/east/1.png")
        self.assertEqual(tuple(east[20, 41, :3]), (255, 220, 90))      # the flash at the muzzle on the shot frame
        self.assertTrue((self.img(self.t / "o/west/1.png") == east[:, ::-1]).all())

    def test_bake_fx_soft_alpha_clips_with_source_over(self):
        body = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
        clear = Image.new("RGBA", (4, 4))
        fx = Image.new("RGBA", (2, 2), (0, 0, 255, 128))
        for name, image in (("body.png", body), ("clear.png", clear), ("fx.png", fx)):
            image.save(self.t / name)
        self.ok("bake_fx", self.t / "body.png", self.t / "clear.png", "--fx", self.t / "fx.png",
                "--at", "0,0", "--anchor", "1,1", "--from", "1", "--out", self.t / "o")
        got = Image.open(self.t / "o/0.png").convert("RGBA")
        expected = body.copy()
        expected.alpha_composite(fx, (-1, -1))
        self.assertEqual(got.tobytes(), expected.tobytes())
        self.ok("bake_fx", self.t / "clear.png", "--fx", self.t / "fx.png", "--at", "0,0",
                "--anchor", "1,1", "--from", "1", "--out", self.t / "clear-out")
        self.assertEqual(Image.open(self.t / "clear-out/0.png").getpixel((0, 0)), (0, 0, 255, 128))

    def test_dir8_rotated_soft_effect_preserves_body_alpha(self):
        src = self.t / "src"
        src.mkdir()
        Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(src / "0.png")
        Image.new("RGBA", (2, 2), (0, 0, 255, 128)).save(self.t / "fx.png")
        spec = {"speck": 0, "flash": {"sheet": "fx.png", "frame_w": 2, "anchor": [1, 1]},
                "dirs": {"east": {"src": "src", "shot": 0, "muzzle": [3, 3], "angle": 90}}}
        (self.t / "spec.json").write_text(json.dumps(spec))
        self.ok("dir8_finish", self.t / "spec.json", "--out", self.t / "o")
        pixels = list(Image.open(self.t / "o/east/0.png").getdata())
        self.assertTrue(all(pixel[3] == 255 for pixel in pixels))
        self.assertIn((127, 0, 128, 255), pixels)


if __name__ == "__main__":
    unittest.main()
