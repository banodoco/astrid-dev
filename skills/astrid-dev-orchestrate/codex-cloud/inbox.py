#!/usr/bin/env python3
"""Read an append-only GitHub issue mailbox; never changes a cursor or issue."""

import argparse
import json
import re
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', help='GitHub owner/repository')
    parser.add_argument('issue', type=int)
    parser.add_argument('--after', type=int, default=0, help='last acknowledged comment ID')
    parser.add_argument('--wait', type=float, default=0, help='maximum wait in seconds')
    parser.add_argument('--interval', type=float, default=30, help='poll interval in seconds')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repository):
        parser.error('repository must be owner/repository')
    if args.issue < 1 or args.after < 0 or args.wait < 0 or args.interval <= 0:
        parser.error('issue and interval must be positive; after and wait must be nonnegative')
    end = time.monotonic() + args.wait
    endpoint = f'repos/{args.repository}/issues/{args.issue}/comments?per_page=100'
    while True:
        try:
            result = subprocess.run(['gh', 'api', '--paginate', '--jq', '.[]', endpoint],
                                    check=True, capture_output=True, text=True, timeout=30)
            comments = [c for c in (json.loads(line) for line in result.stdout.splitlines())
                        if c['id'] > args.after]
            comments.sort(key=lambda c: c['id'])
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError,
                ValueError, TypeError, KeyError) as exc:
            print(f'Inbox read failed: {exc}', file=sys.stderr)
            return 1
        if comments or time.monotonic() >= end:
            print(json.dumps([{'id': c['id'], 'author': c['user']['login'],
                               'created_at': c['created_at'], 'url': c['html_url'],
                               'body': c['body']} for c in comments], ensure_ascii=False))
            return 0
        time.sleep(min(args.interval, max(0, end - time.monotonic())))


if __name__ == '__main__':
    sys.exit(main())
