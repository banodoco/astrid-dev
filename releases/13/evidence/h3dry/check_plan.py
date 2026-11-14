#!/usr/bin/env python3
"""Check archived stdout plan + its captured compiled graph. Exit 0 pass / 1 fail."""
import json
import sys
from pathlib import Path


def main():
    # Usage: check_plan.py <stdout.json> <workflow.vibe.json> <steps> <on|off>
    plan_path, graph_path, steps, turbo = sys.argv[1:]
    assert turbo in ('on', 'off'), 'turbo must be on/off'
    d = json.loads(Path(plan_path).read_text())
    g = json.loads(Path(graph_path).read_text())
    classes = [n['class_type'] for s in g['custody']['scopes'] for n in s['nodes']]
    assert d['status'] == 'ready' and not d['issues'] and not d['fixes']
    b = d['entry']['bindings']
    assert b['steps'] == int(steps), b
    assert b['seed'] == 42, b
    lora = 'LoraLoaderModelOnly' in classes
    weights = [m['name'] for m in d['entry']['requirements']['models']]
    assert lora == (turbo == 'on'), classes
    assert any('turbo' in m.lower() for m in weights) == (turbo == 'on'), weights
    if turbo == 'on':
        assert b['guidance'] == 0.95, b
    else:
        assert 'guidance' not in b, b
    print(f'PASS: steps={steps} seed=42 turbo={turbo} LoraLoaderModelOnly={lora}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
