# JSON decode recursion boundary

The independent review compares VibeComfy base `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` and head `675f5dc2658197318a95e0e1b7c5b232b17cd9d5` on CPython 3.11.18 with the default recursion limit of 1000. The reviewer adds one ignored metadata value to a private copy of the shipped ImageResizeKJ provider.

| Depth | Base | Head | Head with memo bound directly |
| ---: | --- | --- | --- |
| 977 | Publishes | Publishes | Publishes |
| 978 | Publishes | Raises `RecursionError` | Publishes |
| 979 | Raises `RecursionError` | Raises `RecursionError` | Raises `RecursionError` |

The original output is in `/root/codex/review-81b/scratch/depth311-{base,head}.log` and `/root/codex/review-81b/scratch/isolated-depth-{base,head}.log`. Every refusal in the table printed `RecursionError maximum recursion depth exceeded while decoding a JSON array from a unicode string False`. The trailing `False` means the final Python member did not exist.

## Stack comparison

Run the following from each of `/root/codex/review-81b/scratch/base` and `/root/codex/review-81b/scratch/head`:

```bash
flock -n /tmp/astrid-timing.lock true && PYTHONPATH=. nice -n 19 ../py311/bin/python - 979 <<'PY'
import traceback
p='../depth.py'
s=open(p).read().replace("                print(depth,type(e)", "                traceback.print_exc()\n                print(depth,type(e)")
exec(compile(s,p,'exec'))
PY
```

The normalized traceback below retains the relevant frames and source locations. Both runs refused and emitted no final Python member.

```text
frame                             base                         head
                                  —                            workflow_bundle.py:3255 wrapped
emit_bundle                       workflow_bundle.py:3247       workflow_bundle.py:3285
_canonicalize_for_v2_pair         workflow_bundle.py:1602       workflow_bundle.py:1603
_build_v2_sidecar                 workflow_bundle.py:1779       workflow_bundle.py:1780
canonical_v2_custody             emit_ready.py:1298             emit_ready.py:1298
_prepare_workflow_for_emit        emit_prepare.py:336            emit_prepare.py:336
_compute_output_variable_names   emit_kwargs.py:447             emit_kwargs.py:447
_schema_output_names_for_unpack   emit_kwargs.py:392             emit_kwargs.py:392
_node_local_arity_check          identity.py:151                identity.py:151
_node_local_arity_check          emit_ready.py:3665             emit_ready.py:3665
_class_fallback_count            emit_ready.py:3640             emit_ready.py:3640
class_output_count               consume.py:908                 consume.py:1134
output_names                      consume.py:854                 consume.py:1080
_resolve_class_type               consume.py:314                 consume.py:529
_load_pack                        consume.py:267                 consume.py:355
_read_pack_at_root                consume.py:281                 consume.py:375
read_json                         generation.py:233             consume.py:186
loads                             json/__init__.py:346           json/__init__.py:346
decode                            json/decoder.py:337            json/decoder.py:337
raw_decode                        json/decoder.py:353            json/decoder.py:353
```

## Direct memo binding control

Run from `/tmp/option-a` at exact head `675f5dc2`:

```bash
flock -n /tmp/astrid-timing.lock true && PYTHONPATH=. nice -n 19 /root/codex/review-81b/scratch/py311/bin/python - 977 978 979 <<'PY'
import traceback
p='/root/codex/review-81b/scratch/depth.py'
s=open(p).read().replace('def main():','emit_bundle = emit_bundle.__wrapped__\ndef main():').replace('                emit_bundle(w,dest,{})','                owner = c._BundleClassMemo()\n                token = c._BUNDLE_CLASS_MEMO.set(owner)\n                try:\n                    emit_bundle(w,dest,{})\n                finally:\n                    owner.revoke()\n                    c._BUNDLE_CLASS_MEMO.reset(token)').replace("if __name__=='__main__': main()",'').replace("                print(depth,type(e)", "                traceback.print_exc()\n                print(depth,type(e)")
exec(compile(s,p,'exec'))
main()
PY
```

```text
977 OK True
978 OK True
979 RecursionError maximum recursion depth exceeded while decoding a JSON array from a unicode string False
```

The command also printed a traceback for 979 with `consume.py:186` on the stack and the decorator frame absent. It runs `main()` after `exec` returns to avoid adding a harness frame at the recursion boundary. The memo, read tracking, and in-emitter validation remained active throughout each call.

## Conclusion

The cold read-set implementation decodes in `consume.read_json`, which occupies the same stack depth as the base's `generation.read_json`. Its before and after observations do not wrap the recursive decoder. The sole additional live frame in this probe is the outer memo decorator at `workflow_bundle.py:3255`, introduced earlier in the branch by `36ea976f`.

A structural repair would enter and exit the memo scope within both public emitters, preserving nested scope and revocation semantics while removing the wrapper frame. Warm or committed fallback may also retain both `consume.read_json` and `generation.read_json` on the stack, so a general repair must check those separately. Moving observations alone cannot restore the boundary. No product changes were made.
