#!/usr/bin/env python3
"""Check that Agent custody tests import fixtures from their pinned Runtime checkout."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"ENV: {message}", file=sys.stderr)
    return 3


def main() -> int:
    if len(sys.argv) != 3:
        return fail("usage: runtime-fixture-preflight.py <agent-checkout> <runtime-checkout>")
    agent_root = Path(sys.argv[1]).resolve()
    runtime_root = Path(sys.argv[2]).resolve()
    expected_package = runtime_root / "runtime_protocol" / "__init__.py"
    fixture_root = runtime_root / "tests"
    fixture_names = ("test_verified_host_launch", "test_remote_worker_activation")

    sys.path.insert(0, str(agent_root))
    try:
        import runtime_protocol
    except Exception as exc:
        return fail(f"could not import runtime_protocol: {exc}")
    actual_package = Path(runtime_protocol.__file__).resolve()
    if actual_package != expected_package:
        return fail(
            "runtime_protocol resolves outside the pinned Runtime checkout "
            f"(found {actual_package}, expected {expected_package})"
        )

    missing = [str(fixture_root / f"{name}.py") for name in fixture_names
               if not (fixture_root / f"{name}.py").is_file()]
    if missing:
        return fail("pinned Runtime producer fixtures are missing: " + ", ".join(missing))

    try:
        import tests
    except Exception as exc:
        return fail(f"could not import Agent tests package: {exc}")
    tests_path = str(fixture_root)
    if tests_path not in tests.__path__:
        tests.__path__.append(tests_path)
    for name in fixture_names:
        try:
            module = importlib.import_module("tests." + name)
        except Exception as exc:
            return fail(f"could not import pinned Runtime fixture tests.{name}: {exc}")
        actual_fixture = Path(module.__file__).resolve()
        expected_fixture = fixture_root / f"{name}.py"
        if actual_fixture != expected_fixture:
            return fail(
                f"tests.{name} resolved outside the pinned Runtime checkout "
                f"(found {actual_fixture}, expected {expected_fixture})"
            )
        print(f"Runtime fixture OK: tests.{name} ({actual_fixture})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
