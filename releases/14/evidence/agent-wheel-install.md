# Agent release wheels at 66c5ee27

## Submitted repair and terminal comparison

Agent #448 at `36ad4bbc` passed both original wheel jobs. Python 3.11 and 3.12 each installed the built wheel, imported Astrid from site-packages outside the checkout, and ran smoke. The full unit comparison retained all 31,064 primary IDs on both sides. Of 93,391 phase and subtest records, two passing temporary-path keys differed in spelling. Four calls recovered and the H3 contribution case failed at the known frame-count check. Both Windows pwsh attempts remain recorded. [Final review](https://github.com/banodoco/astrid-agent/pull/448#issuecomment-7046585069)

The terminal merge-tier verdict failed with 1,934 findings and 11 unknowns. It normalized 17 suites across 14 of 19 required jobs. All 13 lost identities matched the plan controls. Both passing wheel jobs reached a separate failure in the trusted reader because their final receipts omitted the installed Runtime identity. The release virtual environment survived smoke, but the final capture inspected the outer interpreter. The first trusted comparison and both attempts' native results remain available. [Terminal verdict](https://github.com/banodoco/astrid-agent/actions/runs/44757477745/artifacts/14654516241) · [Runtime identity follow-up](https://github.com/banodoco/astrid-dev/issues/984#issuecomment-7045972955)

## Original diagnosis


**The unchanged capture wrapper reproduced the failed install on both Python minors.** Its PYTHONPATH construction appends an empty component when the parent path is unset. Python interprets the component as the current working directory. During wheel installation the checkout contains the 0.1.0 distribution metadata created by the build. Pip under that environment reports the same version already installed. The original import from the runner temp directory then cannot find astrid. The hosted jobs establish the sequence, while the controlled local comparison isolates the mechanism. The native logs do not print pip's selected metadata path. [Capture source](https://github.com/banodoco/astrid-agent/blob/66c5ee27/scripts/ci/ceiling_capture.py#L103) · [CI install and smoke](https://github.com/banodoco/astrid-agent/blob/66c5ee27/.github/workflows/ci.yml)

| Native job | Python and pip | Verified retained artifact SHA-256 |
| --- | --- | --- |
| [3.11](https://github.com/banodoco/astrid-agent/actions/runs/44682589147/job/136109275140) | 3.11.18 and 24.0 | [14607850680](https://github.com/banodoco/astrid-agent/actions/runs/44682589147/artifacts/14607850680) · 6ea472489f9a6224b70bd8fd9462e5d6b31f031131a509f532b3e80fb9f4ca62 |
| [3.12](https://github.com/banodoco/astrid-agent/actions/runs/44682589147/job/136109275116) | 3.12.16 and 25.0.1 | [14607535979](https://github.com/banodoco/astrid-agent/actions/runs/44682589147/artifacts/14607535979) · 74034b1f69c920c0f18626ea2988537634c171070313c96518ba9c05c3307524 |

Each hosted build wrote astrid.egg-info/PKG-INFO and recorded the same 1,352 archive members, including 1,341 under astrid/ and astrid/__init__.py. Each pip check passed, the clean-directory import exited 1, and neither job reached smoke. The retained step archives contain the commands and outputs through step 06. I rebuilt from the exact source with its hashed build lock and compared the wheel ZIP name set to both native build listings. All 1,352 names matched. The hosted wheel bytes were unavailable.

**Controlled local comparison.** In isolated macOS venvs using 3.11.18/pip 24.0 and 3.12.9/pip 25.0.1, I ran the original wheel install and outside-checkout import against the same rebuilt wheel. Both minors produced all five outcomes below. Local metadata inspection sees astrid.egg-info in the build directory and no Astrid distribution in a clean venv outside it before install. The comparison isolates installation, with dependency provisioning and downstream smoke outside its scope.

| Condition | Native command outcome reproduced locally |
| --- | --- |
| Original capture wrapper, parent PYTHONPATH unset | Install skipped, import failed |
| Ordinary shell, same path with explicit trailing empty component | Install skipped, import failed |
| Original wrapper, parent PYTHONPATH contains only the capture directory | Installed, import passed from venv site-packages |
| Ordinary shell, capture directory only | Installed, import passed from venv site-packages |
| Ordinary shell, no inherited PYTHONPATH | Installed, import passed from venv site-packages |

**Route the correction to the Agent K2/K3 capture owner under #984.** AT3 already names both release-wheel smoke jobs as acceptance. Its historical entries.py ImportError occurs later and needs its own evidence if it reappears. The shared wrapper can preserve the capture directory and existing nonempty caller path without introducing a new empty component. Stop local diagnosis here. On a reviewed candidate require the unchanged 3.11 and 3.12 jobs to install, import from outside the checkout, execute the original smoke command and record its actual result. Require native receipt collection and independent approval for a protected change. Count the jobs only after trusted normalization and adjudication of their real outcomes. [Gate owner tracker](https://github.com/banodoco/astrid-dev/issues/984) · [AT3 task](https://github.com/banodoco/astrid-dev/blob/98498bc3/plans/39-green-mains/tasks.md)
