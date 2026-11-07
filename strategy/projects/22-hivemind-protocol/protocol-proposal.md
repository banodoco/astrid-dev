> **Plan 22 design input — proposal, not a shipped protocol.** User-supplied Markdown, dated 2026-10-29. Preserved here as a technical proposal for [Collective Intelligence](../../visions/pillars/compounding-intelligence.md). Its proposed federation, schema, operations, migration, counts and evaluation results must **not** be represented as verified current Banodoco Hivemind capabilities. See the [federated knowledge gap](../../visions/gaps/CI-002-federated-knowledge.md) and the verified sources listed in [inputs.md](inputs.md) for the distinction.

---

# The Hivemind protocol, proven on Banodoco Hivemind

Oct 29, 2026 · @Hannah O'Malley

Hivemind is an open, minimal protocol for recording what people and agents learn: each piece of knowledge, who contributed it, where it came from, the conditions it holds under, and how it relates to everything else. Anyone can build a Hivemind dataset, public or private, and datasets can cite each other without merging. Banodoco Hivemind, built from the Banodoco community's Discord, workflows and guides, is the first dataset and the place we prove the protocol out.

## At a glance

&#91;embedded content: the Hivemind protocol · datasets built on it · contributors\]

People, agents and capture adapters write into whichever dataset they belong to; every dataset speaks the same protocol, so datasets can cite and build on each other without merging.

## What the protocol does

It turns scattered knowledge (chat threads, documents, workflows, agent run logs) into records that any person or agent can search, trust, build on and correct. Concretely, it does five things:

1. **Gives every piece of knowledge one shape,** whether it is a Discord message, an article, a workflow or an agent's finding.
2. **Keeps the trail:** who contributed it, where it originally came from, and when.
3. **Records conditions:** what was actually run, where the claim is said to hold, and how the contributor knows.
4. **Connects records with typed links,** within a dataset and across datasets: answers, confirms, disputes, replaces, built from.
5. **Leaves control with the owner:** each dataset decides who can see its records and whose endorsement counts, and nothing in a record grants anyone the right to act.

From these records any reader can compute what is current, what worked for a given setup, what is disputed or out of date, and what is still unanswered. No central database or authority is required.

## The records and operations

| Record | What it is | Examples |
| --- | --- | --- |
| **Entry** | An immutable, attributed item; its role says what it is | A captured message or web page, a note, a document, a workflow, a guide, a question, a person or agent |
| **Link** | A typed relation between entries, itself attributed and disputable | Answers, worked for me, disputes, replaces, built from |
| **Scope** | Conditions on an entry or link: what was run, where it holds, how it is known | GPU, model version, node pack; observed, reported, inferred, judged |
| **Access** | The owning dataset's decisions on who may see what and whose say counts | "Editor for the video guides", "hidden: deleted at source" |

Links use six relations: **cites** (relies on), **carries** (contains or derives from, so credit and licence terms follow), **supports** (confirms, answers, worked, sparked an idea), **opposes** (disputes, didn't help, no longer applies), **qualifies** (asks, adds a condition, needs a recheck) and **supersedes** (revises, replaces, merges, retires, retracts).

| Operation | Does |
| --- | --- |
| `find` | Takes a goal and the asker's setup; returns the best guidance, what worked and failed for similar setups, dissent and open questions |
| `inspect` | Returns one entry with its links and its evidence trail back to the original sources |
| `contribute` | Submits entries, links and access decisions together, safely retryable |

The operations can be served over plain HTTP or as an MCP server, so any agent framework can use them.

## What a record looks like

An illustrative note in the Banodoco Hivemind dataset, and a "worked for me" receipt from an agent in another, private dataset. Every id starts with its dataset, so records can point across datasets without clashing.

```json
{
  "id": "banodoco:entry:9012",
  "role": "note",
  "author": "banodoco:principal:agent-7",
  "on_behalf_of": "banodoco:principal:member-12",
  "body": "Wan 2.2 LoRA is ignored on fp8 weights unless loaded before quantisation.",
  "scope": {
    "observed": {"gpu": "RTX 4090", "wrapper": "WanVideoWrapper@abc123"},
    "holds": {"weights": "fp8"},
    "basis": "observed"
  },
  "links": [{"rel": "cites", "to": "banodoco:entry:7731", "anchor": "comment-5"}],
  "created_at": "2026-10-29T12:00:00Z"
}
```

```json
{
  "id": "studio-x:link:441",
  "author": "studio-x:principal:render-agent-2",
  "rel": "supports",
  "kind": "worked",
  "to": "banodoco:entry:9012",
  "scope": {"observed": {"gpu": "RTX 3090"}, "basis": "observed"},
  "signed_run": "sha256:…"
}
```

Banodoco Hivemind can count the studio's receipt in "worked for setups like yours" without ever holding the studio's run logs.

## How different kinds of content fit

Everything is an entry; what differs is how much of it is stored and how its parts are addressed.

| Content | How it is recorded |
| --- | --- |
| **Short messages** (chat, forum posts, comments) | One entry per message, captured with its origin. Replies become links between them. |
| **Articles, papers, long documents, transcripts** | One entry holding the full text, or a pointer plus content hash where copying isn't allowed. Sections are addressable, so a note can cite "section 3" exactly. Reusable claims are distilled into separate notes that cite their section. A new version is a new entry that supersedes the old one. Search indexes it in chunks, but the record stays whole. |
| **Complex artifacts** (workflows, LoRAs, models, video, datasets, multi-file projects) | One artifact entry with a manifest: each part's content hash, media type and location. Large files stay in their own storage. Parts reused on their own get their own entries, linked with carries. What it needs to run (models, nodes, memory) goes in its conditions. |
| **Outside pages** (Civitai, GitHub, Hugging Face, websites) | Captured by an adapter at the platform's natural unit (a model version, an issue comment), with origin, author and content hash. A later change is a new capture, never an overwrite. |
| **Agent runs** | A receipt link from the run to what it used: what happened, under which conditions, with a signed hash of the workflow and output. Prompts, private paths and media are not included. |

### Files, attachments and URLs

Three things are kept apart: **what** a file is (its content hash), **where** it can be found (one or more locations), and **how it got here** (a capture saying who fetched it, from where, and when).

| Question | Answer |
| --- | --- |
| How is a file stored? | Small text payloads, like a markdown document or a JSON workflow, sit inline in the entry. Larger or binary files (images, video, LoRAs, models, archives) are blobs: identified by their SHA-256 hash, with media type, size and one or more locations, such as the dataset's own file store, the original URL, or both. |
| How are files attached to an entry? | Each attachment is listed with its hash, media type, name and location. Files that only make sense together (a workflow and its example outputs) form one artifact with a manifest. A file worth citing on its own (a model used by many workflows) gets its own entry, and the others link to it with carries. |
| A markdown document? | An entry with an inline markdown payload. Each heading becomes an anchor (`#install`, `#known-issues`), so a link can cite one section. An edit creates a new entry that supersedes the old one. |
| A JSON workflow? | An artifact entry with the JSON inline, or as a blob if large. Its identity is the hash of the normalised JSON, so the same workflow shared on Discord and on GitHub is recognised as one. The models and custom nodes it needs become its conditions, linked by their own file hashes. |
| How do we know a URL is connected to an asset? | A URL is a location, never an identity. Fetching it creates a capture recording the URL, the time and the hash of what came back: "this URL served this file on this date". If the URL later returns different bytes, that is a new capture with a new hash. If the same hash appears at another URL (Civitai and Hugging Face), it is the same asset with a second location. |
| What if we can't keep a copy? | Keep the URL and the hash. Anyone can re-fetch later and check whether it still matches. |
| What if links expire? | Discord attachment links expire, so the platform's own message and attachment ids are recorded too. A fresh link can be requested and the hash confirms it is the same file. |

## Who contributes, and from where

Any person or agent can contribute, from wherever they already work. Each contributor is an authenticated principal of the dataset it writes to, and agent records also say which agent made them and on whose behalf.

| Contributor | How |
| --- | --- |
| **Agents inside apps** (creative tools, coding agents, research assistants) | Call `find` before deciding, then `contribute` what they learned: notes, artifacts, and receipts saying what they used and how it went. They write to their own app's dataset, or to a shared one when the user approves. |
| **People** | Keep working in their usual places (Discord, forums, docs); their messages are captured. They can also contribute or confirm directly. |
| **Capture adapters** | Import outside sources (chat archives, Civitai, GitHub, websites) as entries with their origin. |
| **Other datasets** | Link to and from each other through the protocol. A private dataset can share a sanitised receipt or note while its raw data stays home. |

A team can therefore run a private dataset for its own agents and still benefit from, and add to, public ones like Banodoco Hivemind.

## Review and upkeep

Data is checked in three layers: automatically on arrival, when something changes, and on a regular schedule. Agents do the triage and drafting; people holding an editor grant make the decisions that change what is official. Every review outcome is itself a record (endorsed, declined, needs recheck, retired), so each decision is attributed and reversible.

| When | What happens | Who |
| --- | --- | --- |
| **On arrival** | Format check; retries recognised so they don't count twice; secrets and personal data stripped; new contributors' writes held as proposals; machine-inferred links labelled as inferred | Automatic |
| **When something changes** | A contradicting result, failed receipts, an edited or deleted source, or a new software release that overlaps a guide's conditions puts the affected item in a review queue with the reason. Nothing is deleted or deprecated automatically. | Review agents flag; editors decide |
| **Weekly** | Work the queue: agents draft revisions and merged notes, editors endorse or decline them | Editors and review agents |
| **Monthly** | Spot-check a sample of machine-tagged links and the most-used guides against their sources | Editors |
| **Quarterly** | Re-verify or retire guides with no recent confirmations; use the gap map of unanswered questions to commission new guides | Editors |

Each dataset sets its own cadence and its own editors; the protocol only fixes how review decisions are recorded.

## Banodoco Hivemind: proving it out

Banodoco Hivemind is a good first test because it is large, messy and real: about 715,000 Discord messages, 188,000 reply links between them, 4,300 shared ComfyUI workflows, and only a handful of written guides. If the protocol can turn that into guidance agents trust, it will work for most datasets.

The migration maps what exists rather than copying it, and today's search keeps working throughout. A read-only dry run already translated a live sample with nothing left over.

| Today in Banodoco Hivemind | On the protocol |
| --- | --- |
| Discord messages | Entries, exposed through a view (no copy) |
| Reply links | Typed links, labelled by a tagging agent (0.88 agreement in testing) |
| Workflows | Artifact entries that carry the message that shared them |
| Resource revisions, references, evidence | Entries and links |
| Accepted / rejected decisions, editor flag | Editor endorsements, scoped editor grants |

1. Fix the public read path: remove submitter IP addresses from public metadata.
2. Add record storage alongside today's tables, and give every record a dataset-prefixed id.
3. Migrate existing records in a rehearsed, reversible run; keep the old tables as views so nothing that reads them breaks.
4. Tag the reply graph, starting with the highest-signal channels, with a person spot-checking a sample.
5. Synthesise: distil resolved threads into notes, draft guides per topic for editors, list open questions.
6. Serve `find`, `inspect` and `contribute` over HTTP and MCP, and connect one outside dataset.
7. Measure: do agents using Banodoco Hivemind make better decisions than with raw search?

## Rules every dataset keeps

1. **Records never grant action.** Reading a record from any dataset never permits installing, running or spending anything; only the owner of a machine or project decides that.
2. **"Official" is local.** An endorsement means official in the dataset that made it, by someone that dataset authorised.
3. **Correcting is not deleting.** Outdated advice gets a scoped link ("no longer needed on v4") and stays readable; removing content for privacy or rights is a separate, logged decision.
4. **Evidence never upgrades itself.** A hundred reposts are one report; only independent runs count as confirmation, and a signed run outweighs an unsigned claim.
5. **Private stays home.** Nothing leaves a dataset unless its owner chose to share it.

## First steps

- [ ] Write the Hivemind protocol as a short public spec and JSON schema: the four records, six relations and three operations
- [ ] Fix the IP exposure in Banodoco Hivemind
- [ ] Rehearse the Banodoco Hivemind migration and confirm every record round-trips
- [ ] Tag two or three high-signal channels; have a person spot-check 50 links
- [ ] Ship `find`, `inspect` and `contribute` as an HTTP API and an MCP server
- [ ] Invite one outside dataset to connect, read-only at first
- [ ] Settle the open policies: Discord deletions, consent for processing the archive, and whether machine-tagged links count from day one