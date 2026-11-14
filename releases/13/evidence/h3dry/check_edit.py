#!/usr/bin/env python3
"""Bounded 24 fps RGB frame checks. Requires Python 3, numpy, ffmpeg/ffprobe.
Exit 0: every requested assertion passed. Exit 1: assertion/input/tool failure.
"""
import argparse
import json
import subprocess
import sys
import numpy as np


def span(value):
    a, b = map(int, value.split('-'))
    if not 0 <= a <= b < 72:
        raise argparse.ArgumentTypeError('range must be within 0-71 (inclusive)')
    return set(range(a, b + 1))


def probe(path):
    data = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height,avg_frame_rate', '-of', 'json', path]))['streams'][0]
    if (data['width'], data['height'], data['avg_frame_rate']) != (1024, 576, '24/1'):
        raise ValueError(f'{path}: expected 1024x576 at 24/1 fps: {data}')


def decoder(path):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-threads', '1', '-i', path,
        '-map', '0:v:0', '-t', '3.1', '-fps_mode', 'passthrough', '-threads', '1',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)


def frame(proc):
    raw = proc.stdout.read(1024 * 576 * 3)
    if not raw:
        return None
    if len(raw) != 1024 * 576 * 3:
        raise ValueError('partial decoded frame')
    return np.frombuffer(raw, dtype=np.uint8).reshape(576, 1024, 3)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main():
    p = Parser(description=__doc__)
    p.add_argument('source')
    p.add_argument('output')
    p.add_argument('--kept', type=span, required=True)
    p.add_argument('--changed', type=span, default=set(), help='each listed frame must differ')
    p.add_argument('--mask')
    p.add_argument('--outside-only', action='store_true')
    p.add_argument('--require-change', action='store_true', help='some inside-mask pixel must differ')
    p.add_argument('--seam', type=int, help='kept prefix must end here; this frame must differ')
    args = p.parse_args()
    if args.outside_only and not args.mask:
        raise ValueError('--outside-only requires --mask')
    if args.require_change and not args.outside_only:
        raise ValueError('--require-change requires --outside-only')
    if args.seam is not None and (not 1 <= args.seam < 72 or args.kept != set(range(args.seam))):
        raise ValueError('--seam requires the exact kept prefix 0-(seam-1)')
    for path in [args.source, args.output]:
        probe(path)
    mask = None
    if args.mask:
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', args.mask,
            '-t', '0.05', '-frames:v', '1', '-threads', '1', '-f', 'rawvideo',
            '-pix_fmt', 'rgb24', 'pipe:1'])
        mask = np.frombuffer(raw, dtype=np.uint8).reshape(576, 1024, 3)[:, :, 0] > 0
        expected = np.zeros((576, 1024), dtype=bool)
        expected[144:432, 384:640] = True
        if not np.array_equal(mask, expected):
            raise ValueError('mask must be white x=[384,640), y=[144,432), black elsewhere')
    procs = [decoder(args.source), decoder(args.output)]
    errors, changed, inside_changed = [], [], []
    count = 0
    try:
        while True:
            a, b = [frame(proc) for proc in procs]
            if a is None or b is None:
                if (a is None) != (b is None):
                    errors.append('source/output frame counts differ')
                break
            diff = np.any(a != b, axis=2)
            if np.any(diff):
                changed.append(count)
            if count in args.kept:
                selected = diff[~mask] if args.outside_only else diff
                if np.any(selected):
                    errors.append(f'protected pixels changed at frame {count}')
            if args.outside_only and np.any(diff[mask]):
                inside_changed.append(count)
            if count in args.changed and not np.any(diff):
                errors.append(f'expected changed frame {count} is identical')
            count += 1
        if count != 72:
            errors.append(f'expected exactly 72 decoded frames, got {count}')
        if args.seam is not None and args.seam not in changed:
            errors.append(f'no change at seam frame {args.seam}')
        if args.require_change and not inside_changed:
            errors.append('no inside-mask pixel changed')
    finally:
        for proc in procs:
            proc.stdout.close()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait()
    # Fully consumed streams normally exit zero. Early termination is already a count failure.
    if any(proc.returncode != 0 for proc in procs) and not errors:
        errors.append('ffmpeg decoding failed')
    print(json.dumps({'result': 'FAIL' if errors else 'PASS', 'frames': count,
        'changed_frames': changed, 'inside_changed_frames': inside_changed, 'errors': errors}))
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
