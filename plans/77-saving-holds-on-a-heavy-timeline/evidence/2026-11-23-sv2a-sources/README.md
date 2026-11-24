# Sources for the SV-2a retained-stack diagnostic

These are references from the completed two-save profile. The files demonstrate direct lifecycle, initial head and legal-gesture verification, an installed pin preparation and the optional sampling helper. They target the preceding v30, two-save experiment. The SV-2a operator needs the current retained head and only one gesture. The source copies are historical references, so the new run needs a separately approved command and exact SHA.

I replaced the measurement workspace's absolute root with `/path/to/astrid-sandbox`. Generated fixture IDs and public proof fields are kept. No credentials, backup authentication fields or host-secret material were found in these sources. `arm-free-space.mjs` and `reused-trace-helpers.mjs` supply the relative browser dependencies. The preparation script generates its manifest through its embedded Node program using the existing App `checkManifest` and Agent pin generator. [App manifest verifier at the exact source](https://github.com/banodoco/astrid-app/blob/846ce8cafdf8ca2e58a101a18242c9e50358f89c/scripts/installer/pin.mjs) [Agent generator at the exact source](https://github.com/banodoco/astrid-agent/blob/b7f0e96a4934ddb4c123eab791a6e18efb8f79ac/scripts/regenerate_runtime_pins.py)

| Source file | Original SHA-256 | Sanitized SHA-256 | Workspace replacements |
| --- | --- | --- | ---: |
| [direct-runtime-up.py](direct-runtime-up.py) | `01a870b4cfec7d6b68c441364e132d75b0e883bfa6fa6825e7c4d94e85093966` | `01a870b4cfec7d6b68c441364e132d75b0e883bfa6fa6825e7c4d94e85093966` | 0 |
| [browser-two-save-profile.mjs](browser-two-save-profile.mjs) | `021fa08e7d333602af6e99021508512cd0c1825b99ef6470cc60fc50b2c6808d` | `021fa08e7d333602af6e99021508512cd0c1825b99ef6470cc60fc50b2c6808d` | 0 |
| [prepare-candidate.sh](prepare-candidate.sh) | `cfd1b62672d1ce09104ece6c050ce4d7926647ea1255a78d4c281ea1c9e4691f` | `6f54923622e5237be6ab9e36b330713b524866ae3248887148cae3a1c75a56fa` | 1 |
| [profile-two-save.mjs](profile-two-save.mjs) | `a8881b68b498bdc790b7ae75d6fb68d36ec1ba89208f0415ab64b28e89c69a46` | `6f074b006f51b8998fbbd60b10b924b4361b1432fc6eb5d55a658309a69fa22a` | 1 |
| [arm-free-space.mjs](arm-free-space.mjs) | `b8d6dc6727a945c0c937221720c1f39c2595fcd0b90eed8f2d7f93584796d2a0` | `b8d6dc6727a945c0c937221720c1f39c2595fcd0b90eed8f2d7f93584796d2a0` | 0 |
| [reused-trace-helpers.mjs](reused-trace-helpers.mjs) | `22b414a947301a47d7666da7e0d2b8e85bd857c5c38efba3e118ec5af0ec36a9` | `f03f943b39d704012d67550d0cf48fe60ac9de42b1f19692ea33f62e17786bb0` | 6 |

[Redacted receipt shapes](SHAPES.md)
