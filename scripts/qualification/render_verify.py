#!/usr/bin/env python3
"""Verify that a rendered video decodes and is what was asked for (qualification items 2b and 2c).

  python3 -I render_verify.py OUT.mp4 --duration 312.5 [--tolerance 1.0] [--width 1920 --height 1080]
        [--fps 30] [--audio] [--color 0.5=#ff0000 --color 1.5=#00ff00] [--min-audio-db -50]
        [--json report.json]

Checks, each reported pass/fail (exit 0 only if all pass; exit 2 on bad usage or missing tools):
  decode     the whole file decodes with no error (`ffmpeg -v error -i F -f null -`), not just the header;
  probe      the container's duration is within --tolerance seconds of --duration; video stream's width,
             height and frame rate match when given; an audio stream exists when --audio;
  frames     the frame count is within one frame of duration x fps when --fps is given;
  color      the pixel at the frame centre at time T is within 12 per channel of the expected #rrggbb (use for
             fixtures with known solid-colour spans);
  audio      the mean volume of the whole audio stream is above --min-audio-db (silence is wrong output).
A render that "finishes" with a zero-length, truncated, black or silent file fails here.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(path):
    p = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path])
    if p.returncode:
        raise ValueError(p.stderr.strip() or "ffprobe failed")
    return json.loads(p.stdout)


def fps_of(stream):
    num, _, den = (stream.get("avg_frame_rate") or "0/1").partition("/")
    return float(num) / float(den or 1) if float(den or 1) else 0.0


def pixel_at(path, t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                        "-vf", "scale=1:1:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    if p.returncode or len(p.stdout) < 3:
        raise ValueError(f"no frame at {t}s: {p.stderr.decode(errors='replace').strip()}")
    return tuple(p.stdout[:3])


def mean_volume(path):
    p = run(["ffmpeg", "-v", "info", "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", p.stderr)
    return None if not m else (float("-inf") if m.group(1) == "-inf" else float(m.group(1)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--duration", type=float, required=True, help="expected duration in seconds")
    ap.add_argument("--tolerance", type=float, default=1.0)
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--audio", action="store_true", help="an audio stream is required and must not be silent")
    ap.add_argument("--min-audio-db", type=float, default=-50.0)
    ap.add_argument("--color", action="append", default=[], metavar="T=#rrggbb")
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args(argv)
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        print("ffmpeg and ffprobe are required", file=sys.stderr)
        return 2
    checks = []

    def check(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    d = run(["ffmpeg", "-v", "error", "-i", a.video, "-f", "null", "-"])
    check("decode", d.returncode == 0 and not d.stderr.strip(),
          "whole file decoded" if d.returncode == 0 and not d.stderr.strip() else (d.stderr.strip()[:400] or "ffmpeg exit " + str(d.returncode)))
    try:
        info = probe(a.video)
    except ValueError as e:
        check("probe", False, str(e))
        info = None
    if info:
        dur = float(info["format"].get("duration", 0))
        check("probe.duration", abs(dur - a.duration) <= a.tolerance, f"{dur:.3f}s vs expected {a.duration}s ±{a.tolerance}")
        v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
        check("probe.video_stream", v is not None, "present" if v else "no video stream")
        if v:
            if a.width:
                check("probe.width", v.get("width") == a.width, f"{v.get('width')} vs {a.width}")
            if a.height:
                check("probe.height", v.get("height") == a.height, f"{v.get('height')} vs {a.height}")
            if a.fps:
                f = fps_of(v)
                check("probe.fps", abs(f - a.fps) < 0.01, f"{f:.3f} vs {a.fps}")
                n = v.get("nb_frames")
                if n and str(n).isdigit():
                    want = round(a.duration * a.fps)
                    check("frames", abs(int(n) - want) <= max(1, round(a.tolerance * a.fps)), f"{n} frames vs about {want}")
        has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
        if a.audio:
            check("probe.audio_stream", has_audio, "present" if has_audio else "no audio stream")
            if has_audio:
                mv = mean_volume(a.video)
                check("audio.level", mv is not None and mv > a.min_audio_db, f"mean {mv} dB, floor {a.min_audio_db} dB")
    for spec in a.color:
        t, _, hexcol = spec.partition("=")
        want = tuple(int(hexcol.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        try:
            got = pixel_at(a.video, float(t))
            check(f"color@{t}s", all(abs(g - w) <= 12 for g, w in zip(got, want)), f"got {got} want {want}")
        except ValueError as e:
            check(f"color@{t}s", False, str(e))
    for c in checks:
        print(("PASS" if c["ok"] else "FAIL"), c["check"], "-", c["detail"])
    if a.json_out:
        json.dump({"video": a.video, "checks": checks, "ok": all(c["ok"] for c in checks)}, open(a.json_out, "w"), indent=2)
    return 0 if all(c["ok"] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
