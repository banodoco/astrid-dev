# Store timeline history without repeating whole document images

Labels `release:15`, `plan:77`

Plan 77’s signed 300-clip sandbox shows how whole-document history increases the bytes read at startup and during save verification. Saving performance work should investigate a durable representation that retains the evidence needed to replay and audit an edit without storing each duplicate document image.

- The signed fixture’s 32-edge read bound covered 427,224,837 bytes in the selected history, receipt and revision fields, or about **13 MB per edge** across this batch-heavy fixture.
- The 12-command accepted edge stores **48 canonical document images for 13 distinct exact values**. Its original and landing vectors contain the same values.
- At this mix, a 1,000-edge startup walk would read about **13.35 GB**. The repeated warm archive read and stored-byte hash took 21.743 s for the byte volume of 992 edges. Actual cold I/O and distinct 1,000-edge startup still need measurement.

Two archived ordinary single-command moves at 288 clips each stored **2.632 MB of measured logical text** across their history, receipt, parent revision, and acceptance event.
An exact 300-clip single-command delta and its physical SQLite/WAL growth remain unmeasured. The 288-clip samples are the closest measured storage comparison.

Scope the successor format against canonical replay, Undo/redo, explicit restore, retained object lifetimes, corruption refusal and independent doctor. Document migration and the installed previous Runtime’s start, doctor and rollback behavior before changing the stored format. Compare physical and logical growth on ordinary single edits as well as sequential batches. Plan 77’s second cut keeps the current history format and will separately measure the content-keyed verification walk. [Raw byte walk](read-hash-cost.json), [single-command storage receipt](single-command-storage.json), [feasibility note](RESULT.md).
