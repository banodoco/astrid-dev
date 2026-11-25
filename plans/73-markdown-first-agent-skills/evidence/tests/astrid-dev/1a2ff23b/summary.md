# MSC-8 — integrated cold start on the final candidate

Candidate head: `1a2ff23b17153b2b160047be0fd882c3596a59a8` (`project/73-markdown-first-agent-skills`), run on a fresh clone of `https://github.com/banodoco/astrid-dev` checked out at that SHA, 25 Nov 2026. `main` was `2c362df89ac710f8eae10a2ced0e906a78790e07`, already merged into the head.

| Step | Command | Result |
| --- | --- | --- |
| Delta check | `git log 2761114f93452d7c3110b71a9b55a5d4dc36490d..origin/main -- skills/` | Four commits (9def7d12, ff119a09, 4a7c93b8, ce5d02d7). All ported: ce5d02d7 and 4a7c93b8/ff119a09 in `evidence/cutover-map-int.md`, 9def7d12 in `evidence/cutover-map-int2.md`. Nothing unported. `skills/` and `sync.sh` no longer exist on the head. |
| Links into the old layout | `git grep -n -E "\]\([^)]*skills/" -- ':!skills' ':!plans/*/evidence'` | Only pinned historical blob URLs remain; the link-rewrite script reports 0 left to rewrite and 0 unmapped. |
| Repository check | `python3 scripts/astrid_dev.py check` | exit 0 |
| Skill packages | `python3 scripts/astrid_dev.py skills check` after `skills build` | exit 0: "Skill packages match their Markdown sources" |
| Reproducible build | `skills build` run twice; sha256 of every generated file except the `repo` symlink | Identical (`264d74d49a4726bc9098da7efc102ae7b40afd2f6236d20d40e319a06ebfe724` both times) |
| Install, two temporary homes | `skills install --dry-run`, then `skills install --destination <h1>/skills --destination <h2>/skills`, then the same again | Dry run printed `would-link`; the install linked 14 packages into each home; the second run printed `already-linked` (idempotent). Each package has `SKILL.md` and a `repo` link. |
| Full unit suite | `python3 -m unittest discover -s scripts -p "test_*.py"` (run on the same tree before the push) | 689 tests OK |
| Shared worker environment smoke | `bash env/smoke.sh agent tests/test_skills.py` from an `astrid-agent` checkout at `c0ad6b54`, with the script taken from the fresh clone | `ENV-PASS agent tests/test_skills.py` (133 passed in 9m27s; runtime 5120462d, vibecomfy 48b5fa9e, lifecycle 9f88ef7640) |

Not covered here, by design: macOS path behaviour and the Codex discovery result, which MSC-7 recorded as NO-RESULT on #1746; both go to R and the completion body as Unproven.
