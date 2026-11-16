# Architectural & Design Decisions (ADRs)

This document explains key technical, structural, and policy decisions made during the design and implementation of the Veloxa CXO Cockpit, detailing alternatives considered, trade-offs evaluated, and defended rationale.

---

## Decision Index

- **ADR-001**: Temporal Point-in-Time Isolation Architecture
- **ADR-002**: Embedded SQLite with Deterministic Fact Graph vs External Vector DB
- **ADR-003**: Epistemic Refusal & Uncertainty Protocol ("I Don't Know" Policy)
- **ADR-004**: Handling CEO Voice Note Requests (Pushback vs Compliance)
- **ADR-005**: 14 Grounded Agent Architecture & Post-Oct 31 Simulation Engine

---

### ADR-001: Temporal Point-in-Time Isolation Architecture

- **Context**: The cockpit must answer queries as of specific dates ("what did we know on date X?"), strictly enforcing release-date boundaries (Day 1: Mon 16 Nov, Day 2: Tue 17 Nov, Day 3: Wed 18 Nov, Day 4: Thu 19 Nov). Future material must never leak into earlier answers.
- **Alternatives Considered**:
  1. *Git branch-per-day or directory switching*: Switch codebase branches or folders on the fly.
  2. *Runtime date-filter over unified store*: Ingest all records with explicit `release_day` and `record_date` attributes, applying strict filtering at query time.
- **Decision**: **Alternative 2 (Runtime temporal filtering with release-day gating)**.
- **Rationale**: Clean, testable, and allows instant comparison between "what we knew on Day 1" vs "what we learned on Day 4" without process restarts or filesystem re-indexing. Every record in SQLite and the fact graph carries `release_day` (1 to 4) and `event_date`. Queries passed with `as_of_day` or `as_of_date` mechanically prune any nodes where `release_day > query_release_day`.

---

### ADR-002: Embedded SQLite with Deterministic Fact Graph vs Vector DB

- **Context**: Storage for records, entity links, evidence index, and citations.
- **Alternatives Considered**:
  1. *External Vector DB (Chroma / Pinecone / Qdrant)* with semantic embedding retrieval.
  2. *Self-contained SQLite database with normalized schema, FTS5 full-text search, and explicit Evidence Index cross-references*.
- **Decision**: **Alternative 2 (Self-contained SQLite + Normalized Fact Graph)**.
- **Rationale**:
  - The dataset comprises ~19 employees, 64 Jira issues, 30 GL rows, 1453 git commits, 11 emails, and 13 incidents. An external vector database introduces opaque non-deterministic hallucination, heavy dependencies, and network fragility.
  - SQLite guarantees 100% deterministic citation tracking, exact entity queries (e.g. employee ID `VX007`), fast regex/text queries, zero-setup reproducibility on any test machine, and perfect auditability.

---

### ADR-003: Epistemic Refusal & Uncertainty Protocol ("I Don't Know" Policy)

- **Context**: The cockpit must state confidence levels, cite specific evidence, and explicitly refuse or admit "the sources disagree" or "I do not know" when facts are missing or contradictory.
- **Policy Formulated**:
  1. **Refuse Unsubstantiated Gossip / Private Espionage**: When asked to read private messages or rank employees by flight risk based on private chatter, refuse on legal, ethical, and factual grounds (citing lack of record and violation of privacy policy).
  2. **Flag Factual Contradictions**: When transcripts state an unsubstantiated figure (e.g. Ananya claiming ₹42 Cr ARR vs Board report ₹5.8 Cr, or Meera claiming ₹2.2L burn vs ₹44L actual), the cockpit presents both sources, cites the exact documents, explains the discrepancy, and tags confidence as **LOW / CONFLICTING**.
  3. **Strict Epistemic Guardrails**: If an event occurred after the queried cutoff date or no data exists in the data room (e.g. "What is our customer churn rate in Germany?"), the engine explicitly replies: *"I don't know: no records in the data room cover this topic."*

---

### ADR-004: Handling CEO Voice Note Requests (Pushback vs Compliance)

- **Context**: CEO voice notes T6a–T6d require written responses. Hackathon rules state: *"Either make the change or push back with your reasons. Agreeing to everything is not a good sign."*
- **Decisions**:
  - **T6a (Top 3 Worries card)**: **Adopt**. Executive dashboards need proactive risk surfacing without manual query burden.
  - **T6b (Marketing reporting to CRO)**: **Adopt with design decoupling**. We build an agile schema supporting matrix and multi-parent reporting lines without breaking historical attribution. We advise postponing active re-routing until CRO contract execution.
  - **T6c (Flight risk ranking & reading Slack messages)**: **STRONG PUSHBACK**.
    - Reading personal employee messages violates data privacy laws and employee trust.
    - Deepa Joshi explicitly opposed deanonymizing team pulse comments in T3/Email 11; Ananya's claim that "Deepa says it's fine" is factually unsupported.
    - The cockpit will instead provide team-level burnout and operational strain metrics.
  - **T6d (Priya's resignation impact on Atlas v3)**: **Adopt with urgent crisis plan**. Detail the severity: Priya represents 40%+ of git commits and single-handedly built the routing engine. Atlas v3 will definitely slip past Dec 15 without immediate intervention.

---

### ADR-005: 14 Grounded Personas & Post-Oct 31 Simulation Engine

- **Context**: 14 people must be represented as interviewable agents grounded in data, with believable personal lives and the ability to autonomously generate plausible daily activity beyond 31 Oct 2026.
- **Decision**:
  - Each agent is modeled with:
    1. Static baseline: Name, ID, role, department, manager, salary tier, join date, location.
    2. Empirical state: Commit patterns, Jira backlog, on-call shifts, pulse sentiment, leave history.
    3. Grounded persona narrative: Work stress, personal life constraints, interpersonal dynamics.
  - A deterministic simulation clock drives daily tick events (e.g. Nov 1 - Nov 15 2026), generating plausible git commits, Jira status updates, on-call ticket responses, and status emails based on their established trajectory (e.g. Priya working notice period and conducting handover sessions; Snehal taking on-call load; Siddharth Mehta departed).
