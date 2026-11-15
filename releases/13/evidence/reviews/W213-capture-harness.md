Committed as `73d15a036746b0fbf9fd52c423027e74b33e84f3`.

```text
$ git diff --stat 60bf5056..HEAD
 scripts/journey_hosted_update.py    |  44 ++++++++++++++-
 scripts/journey_update_button.mjs   | 106 +++++++++++++++++++++++++++++++++++-
 tests/test_journey_hosted_update.py |  33 +++++++++++
 3 files changed, 179 insertions(+), 4 deletions(-)
```

The new `update-button.json` keys have these examples from the test fixture:

- `door_responses`: `{"method":"GET","path":"/health","status":200,"body":{"release":2,"instance":"a"}, …}`
- `door_responses_dropped`: `0`
- `door_failures`: `{"t":2,"method":"GET","path":"/health","errorText":"reset"}`
- `session_storage`: `{"t":3,"moment":"after_load","session":{"release":"1"},"local_keys":["tour"]}`
- `console`: `{"t":4,"type":"log","text":"hello"}`; `console_dropped`: `0`
- `dom_snapshots`: `{"t":3,"moment":"after_load","quiet_update_notice":[],"update_elements":[],"settings_updates":[],"body_text_has_updated_line":false}`
- `samples`: `{"t":5,"url":"https://astrid.haus/","release":2,"quiet_update_notice_exists":false,"body_text_has_updated_line":false}`; `samples_dropped`: `0`
- `evidence_dropped`: `{}` when no size trimming is needed.

`node --check scripts/journey_update_button.mjs` passed. The single requested pytest invocation **did not run the tests**: `/usr/local/bin/python3` has no `pytest` module. The new fixture and helper tests therefore remain unverified.

The assertion, timeouts, click flow, and exit codes are unchanged: see the [update-line regex](/home/user/wt/harness32/scripts/journey_update_button.mjs:24), [click and request waits](/home/user/wt/harness32/scripts/journey_update_button.mjs:194), [live assertion](/home/user/wt/harness32/scripts/journey_update_button.mjs:234), and [exit status](/home/user/wt/harness32/scripts/journey_update_button.mjs:263).