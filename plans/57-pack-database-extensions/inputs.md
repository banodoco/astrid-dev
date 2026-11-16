# Inputs — Packs extend the database

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner gave the direction on 15 November 2026 (quoted in [plan.md](plan.md#outcome-and-scope)) and said it is "one for after this stuff is done". Next: after the prior-art read, present the real options (which store, what is protected, how updates and removal treat pack data) and record her choice.

**Prior art:** Pending — nothing inspected yet. Next: trace how the Runtime and the App define, migrate and protect stored data today; how packs install, update, roll back and are removed; where references are handled; and how other extensible tools let extensions own data safely.

**Approach:** Pending — Next: compare namespaced pack-owned tables with declared migrations against a generic document store per pack, and against doing less (pack data kept in files).

**Challenge:** Pending — this touches data safety, updates and a cross-repository contract, so an independent critique is required before greenlight. Next: write the plan, then have it critiqued against the code.

**Proof and limits:** Pending — Next: define the destructive cases to test (drop, alter or delete outside a pack's own tables; a failed migration; removal with data) and what is promised on rollback.

**Review rounds:** Pending — Next: recommend after the design exists; a data model that other packs build on likely needs one review stop after the design and one final round. The owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, and the advisor session.

## Owner decisions

To be numbered after the prior-art read. Known already:

- **D1 Which store.** The Runtime's project database, the App's, or both.
- **D2 What is protected.** Which of Astrid's own tables and fields a pack may read, and which it may never change.
- **D3 How free.** Whether a pack may only add its own tables and rows, or may also add to Astrid's tables.
- **D4 What moves first.** Which core feature becomes the first default-installed pack; the owner's example is references.

## Source identities

None yet.

## References

- The owner's direction, 15 November 2026, in the advisor's session; summarised in [plan.md](plan.md#outcome-and-scope).
