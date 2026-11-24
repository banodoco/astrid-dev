# US-0 baseline on a real install

What it is: a script that times a few ordinary Astrid commands on the owner's own computer, where Astrid is installed and ComfyUI runs, so Plan 81 knows what "today's time" really is on a real install. Container timings are working evidence only; this is the number the release notes can use.

Why only the owner can run it: it needs the installed (published) Astrid and a real ComfyUI on one machine.

What it does: creates one scratch project and timeline, then runs 15 fresh `astrid` processes, each timed: 5 `generate image` with the same prompt, 5 `generate image` with changed prompts, 5 timeline edits. The generations are queued with `--no-wait`, so the script does not wait for images; it queues 10 real image generations on the owner's ComfyUI. Nothing is paid unless the owner's image route is a paid one. It uses no flag that only newer builds have, so it works on what is installed today.

Run (from a terminal on that computer; takes about 10 to 20 minutes):

    export ASTRID_CMD="$(command -v astrid)"
    export COMFY_URL="http://127.0.0.1:8188"        # the address ComfyUI answers on
    export MEDIA_PNG="/absolute/path/to/any-image.png"
    export EVIDENCE_DIR="$HOME/us0-published-$(date +%Y%m%d-%H%M)"
    python3 us0-published.py

Optional: `GEN_EXTRA="--mode t2i --timings"` if `astrid generate --help` lists `--timings` (the per-stage breakdown helps rank the remaining work on an installed profile). Send back the `summary.json` in `EVIDENCE_DIR` (or zip the folder).
