RE1a pin update evidence bundle

- source-fetch-attempts.txt and canonical-fetch.*: local partial-clone transfer failure followed by successful canonical exact-SHA fetch.
- source-verification.txt: exact source and installed Agent checkout verification.
- installed-module-provenance.txt: installed Python import path.
- environment-python.txt, environment-pip-freeze.txt, node-version.txt, typescript-version.txt: actual runtime environment versions captured without reset.
- proof1.command.txt, proof1.stdout-stderr.log, proof1.exit-status: focused operation-handle proof; 3 passed.
- proof2.command.txt, proof2.stdout-stderr.log, proof2.exit-status, proof2-interpretation.txt: exact RE2 candidate acceptance command; declared xfails and no behavioral passes.
- patch.diff and commit-and-tree.txt: one-line patch, local commit and resulting tree.

CORRECTION (RE1a/RE4ab qualified tooling): The earlier source-verification claim that Agent was editable was incorrect and is superseded. The retained installed-module-provenance and pip-freeze show a non-editable site-packages installation; the checkout update alone did not qualify its installed bytes. Earlier proof results remain as historical observations with that limitation. Agent was subsequently force-reinstalled from the verified R12 checkout with --no-deps, then installed timeline files and imports were checked against the exact Git tree without prepending the checkout to sys.path. See ../re1a-re4ab-tooling/ for the correction, raw evidence and new focused proofs.
