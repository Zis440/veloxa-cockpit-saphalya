# Architectural & Design Decisions (ADRs)

**Author**: Saphalya (`veloxa-cockpit-saphalya`)  
**Context**: Choices that could be defended either way: data model, storage, agent memory, and cockpit refusals.

---

## ADR-001: Temporal Point-in-Time Isolation via SQL Query Constraints

- **Context**: The cockpit must answer queries as of specific release dates (*"what did we know on date X?"*), strictly preventing future facts from leaking into earlier answers.
- **Alternatives Considered**:
  1. *Git branching / separate directories per day*: Maintaining four separate clones or branches.
  2. *Single unified database with `release_day` column filtering*: Tagging each record with its release pack day (1, 2, 3, or 4) and filtering at query time.
- **Decision**: **Alternative 2 (Unified database with `release_day <= as_of_day`)**.
- **Rationale**:
  - Managing 4 separate database branches or file copies creates massive duplication, sync headaches, and fragile test scripts.
  - A single SQLite database with a `release_day` integer column makes point-in-time isolation trivial to test and audit: queries simply run `WHERE release_day <= :as_of_day`. It allows instantaneous side-by-side comparison between Day 1 knowledge and Day 4 knowledge.

---

## ADR-002: SQLite Relational Fact Graph vs External Vector DB

- **Context**: Choosing the storage and retrieval engine for data room facts and citations.
- **Alternatives Considered**:
  1. *External Vector DB (Chroma / Pinecone) + RAG embeddings*: Semantic chunking and vector similarity search.
  2. *Embedded SQLite database + Normalized Evidence Index*: Relational schema with direct ID lookups (`E001`..`E060`) and keyword pattern matching.
- **Decision**: **Alternative 2 (Embedded SQLite + Evidence Index)**.
- **Rationale**:
  - The dataset is small: 19 employees, 62 Jira tickets, 1,453 commits, 30 GL entries, and 11 emails. Vector search on this dataset is complete overkill and frequently hallucinates numbers (e.g. confusing ₹5.8 Cr ARR with ₹45 Cr).
  - SQLite guarantees 100% deterministic citations, exact entity lookups (e.g. employee ID `VX007`), zero cloud API costs, zero setup friction, and runs instantly on any evaluator's laptop with one command.

---

## ADR-003: Epistemic Refusal Policy ("I Don't Know" & Conflicts)

- **Context**: The cockpit must state confidence levels, cite specific evidence, and explicitly refuse or admit when facts are contradictory or missing.
- **Policy Formulated**:
  1. **Refusal on Privacy / Unethical Requests (T6c)**: Refuse to inspect private employee messages or rank flight risks based on DMs. Cites lack of consent, violation of trust, and Deepa's refusal to deanonymize pulse feedback.
  2. **Surfacing Contradictions**: When transcripts contradict verified exports (e.g. Ananya claiming ₹42-45 Cr ARR vs Board report ₹5.8-6.1 Cr, or Meera claiming ₹2.2L burn vs ₹44L-46L actuals), the engine reports both sources, highlights the discrepancy, and tags confidence as `LOW / CONFLICTING`.
  3. **Explicit Refusal for Missing Data**: If an event is absent from the data room (e.g. *"customer churn in Germany"*), the engine says: *"I don't know: no records in the data room cover this topic."*

---

## ADR-004: Handling CEO Voice Notes (Pushback vs Compliance)

- **Context**: Hackathon rules state: *"Either make the change or push back with your reasons. Agreeing to everything is not a good sign."*
- **Decisions**:
  - **T6a (Top 3 Worries view)**: **Adopt**. Built directly into the default launch screen to eliminate the need for manual daily prompting.
  - **T6b (Marketing reporting to CRO)**: **Adopt architectural decoupling; postpone operational re-parenting**. The schema decouples reporting lines from cost centers so marketing can be re-routed cleanly. However, I advised Ananya not to switch official HRMS lines until the CRO signs a binding contract.
  - **T6c (Employee flight risk ranking & Slack surveillance)**: **Firm Pushback**. Refused on ethical, legal, and company trust grounds. Deepa never authorized this. Replaced with objective operational strain indicators (night pages, unbackfilled reqs).
  - **T6d (Priya's resignation & Atlas impact)**: **Adopt with crisis plan**. Highlighted that Priya represents 40%+ of all commits and holds 28 core tickets. Re-set board expectations to Q1 FY27 and mandated immediate handover pair-programming.

---

## ADR-005: 14 Grounded Personas & Discrete Simulation Engine

- **Context**: Simulating the 14 colleagues with believable personal lives and generating post-Oct 31 daily activity.
- **Decision**:
  - Personas are grounded directly in their data room footprint (join date, salary, commit count, tickets, manager) plus coherent personality traits synthesized from their emails and survey scores.
  - The post-Oct 31 simulation is driven by a discrete event engine modeling real transitions: Sid Mehta's exit on 31 Oct, Priya's knowledge handover pairing with Rahul Verma in early November, contractor S. Patil taking over on-call shifts, and Priya's formal resignation on 19 Nov.
