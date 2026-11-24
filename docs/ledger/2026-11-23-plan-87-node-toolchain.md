Date: 2026-11-23
Kind: papercut
Source: Plan 87 run, Agent starting inventory
Resolved by: —

The shared Agent test launcher clears the caller's PATH and does not provision the Remotion-pinned Node version or forward a system-CA choice. The starting render inventory initially failed on the host's newer Node and then on the proxy certificate; it passed the four backend renders after a worker-local Node 20.19.4 shim used the system CA without disabling verification. Teach the runner to provision and select the repository's pinned Node and the system trust store explicitly, and report their versions before tests, so baseline failures distinguish setup from product behavior.
