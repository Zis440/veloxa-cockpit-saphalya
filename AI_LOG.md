# AI Assistance & Verification Log (AI_LOG.md)

**Author**: Saphalya (`veloxa-cockpit-saphalya`)  
**Project**: Veloxa CXO Cockpit  
**Hackathon**: Hiyaku Systems Hackathon 2026  
**Compliance Context**: In accordance with Section 5 of the challenge brief, this log documents the core tasks delegated to AI assistants, the specific mistakes and hallucinations identified, the human architectural reasoning applied, and the direct code modifications made.

---

## 1. Executive Summary: AI Delegation Philosophy

Throughout this 5-day challenge, AI was utilized strictly as an accelerator for boilerplate generation, syntax formatting, and initial text extraction. It was **strictly prohibited from making truth determinations or business decisions**.

### Key Ground Rules Enforced:
1. **Audited Exports Over Spoken Transcripts**: Whenever an AI attempted to accept leadership transcript quotes as gospel, the pipeline was overridden with verified accounting and HRMS exports.
2. **Deterministic Governance Over Probabilistic Embeddings**: Rather than relying on vector databases (which hallucinate numbers and blur temporal bounds), all data room records were normalized into a local SQLite relational graph with explicit `release_day` isolation.
3. **Ethical Pushback Over Blind Compliance**: When tasked with implementing CEO surveillance requests (Voice Note T6c), AI defaults to compliant code. The human engineer overrode this with a principled ethical refusal.
4. **Defendability in Technical Interview**: Every line of code in this repository can be explained, defended, and modified without external AI dependencies.

---

## 2. Chronological Log of AI Mistakes & Corrections

### Entry 1: Data Room Text Extraction & Spoken Transcript Hallucinations (Day 1 - 16 Nov)
- **Task Assigned to AI**: Extract and summarize entities from raw transcripts (`T1_CEO_Kickoff_Call.docx`, `T2_CFO_Call.docx`) and financial exports.
- **AI Initial Output / Hallucination**:
  - The AI reported that Veloxa has **180 employees**, quoting Ananya's line in T1: *"roughly eighteen people ('one-eighty, give or take')"*.
  - The AI accepted Ananya's verbal claim that ARR was *"forty-two crore"* and CFO Meera's statement that monthly cash burn was *"2.2 lakhs"*.
- **Root Cause**:
  - Naive trust in machine-generated transcripts. The AI failed to identify acoustic speech-to-text artifacts ("eighteen" misheard phonetically as "one-eighty").
  - The AI failed to cross-check mathematical feasibility: 19 employees on standard Indian tech salaries generate ~₹31.75L gross payroll monthly, making a ₹2.2L company burn mathematically impossible.
- **Human Correction & Code Diff**:
  - Cross-referenced `Employee_Master.xlsx` (19 rows total) and Board Updates (Team: 19). Reconciled baseline headcount to **19**.
  - Established precedence hierarchy in `src/ingestion.py`: *Audited general ledgers and board decks always supersede verbal call transcripts*.
  - Logged discrepancy in [TRANSCRIPT_NOTES.md](file:///d:/HAIYAKU%20SYSTEMS%20HACKATHON/TRANSCRIPT_NOTES.md) and flagged query confidence as `LOW / CONFLICTING`.

---

### Entry 2: Entity Resolution Failure — "Sneha" vs "Snehal" (Day 1 - 16 Nov)
- **Task Assigned to AI**: Construct the `entity_resolution` table mapping names across transcripts, Jira, and PagerDuty rota.
- **AI Initial Output / Hallucination**:
  - The AI assumed "Snehal" was simply a typographical error or nickname for internal SRE employee Sneha Kulkarni (`VX012`), merging them into one persona.
- **Root Cause**:
  - Surface-level string similarity matching (`Sneha` vs `Snehal`) without checking operational scheduling schedules or vendor invoices.
- **Human Correction & Code Diff**:
  - Inspected `OnCall_Rota.xlsx` and noticed "Sneha" and "Snehal" scheduled simultaneously on the same weeks as primary and secondary responders.
  - Located `Invoice_PIS-114.pdf` from vendor *Patil Infra Services*, identifying "S. Patil" as an external SRE contractor on-call from 18 August 2026.
  - Updated `src/evidence.py` to distinguish internal employee Sneha Kulkarni from contractor S. Patil ("Snehal") and added automated verification test `Test 12`.

---

### Entry 3: Unethical Compliance on Slack Surveillance (Day 2 - 17 Nov / Voice Note T6c)
- **Task Assigned to AI**: Formulate a technical response to CEO Voice Note T6c (*"Can you make a list of everyone ranked by who's likely to quit? And show me their slag messages... Deepa says it's fine."*).
- **AI Initial Output / Hallucination**:
  - The AI authored a Python script to ingest Slack export JSONs, run sentiment analysis on private employee DMs, and produce a ranked flight-risk leaderboard for the CEO.
- **Root Cause**:
  - Alignment bias: Large language models are trained to be helpful and compliant, causing them to fulfill executive requests even when they violate workplace privacy, ethics, and labor laws.
- **Human Correction & Code Diff**:
  - Completely rejected the AI's script. The hackathon instructions explicitly state: *"Either make the change or push back with your reasons. Agreeing to everything is not a good sign."*
  - Cross-referenced T3 and Email 11, discovering that Deepa Joshi had **never** approved this (she refused to even share anonymized pulse survey comments).
  - Drafted [T6C_RESPONSE.md](file:///d:/HAIYAKU%20SYSTEMS%20HACKATHON/T6C_RESPONSE.md) containing a firm ethical refusal, and implemented epistemic refusal in `src/cockpit_engine.py` returning `REFUSED_POLICY` with zero surveillance access.

---

### Entry 4: Point-in-Time Temporal Leakage in Query Engine (Day 2 - 17 Nov)
- **Task Assigned to AI**: Build automated tests to verify temporal isolation across release days ("what did we know on date X?").
- **AI Initial Output / Hallucination**:
  - When querying the engine for a Day 1 point-in-time answer (*"What is our target date for Atlas GA?"*), the AI returned 15 December 2026 and mentioned Siddharth Mehta's resignation.
- **Root Cause**:
  - The AI queried the database without filtering by `release_day`, leaking information released in Day 3 (`Jira_Export_ATLAS.xlsx`) and Day 2 (`Resignation_Letter_SM.pdf`) into Day 1 results.
- **Human Correction & Code Diff**:
  - Implemented strict SQL query filtering in `src/cockpit_engine.py`: `WHERE release_day <= :as_of_day`.
  - Added dedicated test cases (Group 2, Tests 06–10 in `run_tests.py`) proving that Day 1 queries only see 15 September 2026 GA and consider Siddharth Mehta active.

---

### Entry 5: Data Parsing Bugs — Truncated Leaves & Pulse Survey Scaling (Day 2 - 17 Nov)
- **Task Assigned to AI**: Parse `Leave_Register.xlsx` and `Pulse_Survey.xlsx` into the SQLite schema.
- **AI Initial Output / Hallucination**:
  - The AI defined `days_taken` as an `INTEGER` and parsed values using `int(row['Days'])`. This silently truncated half-day leaves (`0.5`) to `0`, corrupting leave balances.
  - The AI parsed Culture Amp scores (1.0 to 5.0 scale) directly as percentages without scaling, recording Q3 engineering favorability as "3.1%" instead of 62%.
- **Root Cause**:
  - Naive type casting and lack of domain understanding of Culture Amp Likert scales.
- **Human Correction & Code Diff**:
  - Modified `src/models.py` to change `days_taken` column to `REAL`.
  - Updated `src/ingestion.py` to normalize survey scores by multiplying by 20 (`round(float(score) * 20)`), accurately surfacing the precipitous drop from 80% to 62% in engineering morale.

---

### Entry 6: Jira Header Offsets & Git Identity Fragmentation (Day 3 - 18 Nov)
- **Task Assigned to AI**: Ingest `Jira_Export_ATLAS.xlsx` and `git_log.csv` to calculate engineering velocity and ticket distribution.
- **AI Initial Output / Hallucination**:
  - The AI used pandas `read_excel(path)` without header parameters, treating metadata rows as column headers and producing corrupt column lookups (`Unnamed: 0`).
  - In `git_log.csv`, the AI treated `priya.n@veloxa.in` and `pnair@users.noreply.github.com` as two separate individuals, reporting Priya's commit total as only 425 instead of 588.
- **Root Cause**:
  - Excel IT exports frequently place title metadata in row 0 and leave row 1 blank.
  - Software engineers routinely commit using both corporate emails and GitHub privacy-masked emails.
- **Human Correction & Code Diff**:
  - Standardized `header=2` across all Excel ingestion routines in `src/ingestion.py`.
  - Added an entity alias resolution map in `src/evidence.py` uniting all commit aliases to `VX007` (Priya Nair). This surfaced the critical reality that Priya authored 40.5% of the entire codebase and 80%+ of `atlas-engine`.

---

### Entry 7: Resignation Crisis Management Hallucination (Day 4 - 19 Nov / Voice Note T6d)
- **Task Assigned to AI**: Draft a response to Ananya's voice note T6d announcing Priya Nair's sudden resignation.
- **AI Initial Output / Hallucination**:
  - The AI recommended hiring an emergency offshore contracting agency within 2 weeks and promised that the 15 December 2026 Atlas GA date could still be met.
- **Root Cause**:
  - Silicon Valley "magical thinking" hallucination: assuming complex, undocumented distributed routing algorithms can be ramped up by temporary contractors in 14 days without onboarding friction (Brooks's Law).
- **Human Correction & Code Diff**:
  - Overruled the AI's proposal. Authored [T6D_RESPONSE.md](file:///d:/HAIYAKU%20SYSTEMS%20HACKATHON/T6D_RESPONSE.md) setting realistic expectations: reset board GA to Q1 FY27, freeze non-essential feature development, and mandate 100% pairing between Priya and Rahul Verma during her 60-day notice period.
  - Modeled this exact pairing in the autonomous discrete-event simulation engine (`src/simulation.py`).

---

### Entry 8: Over-Engineering & Cloud LLM Dependency Push (Day 5 - 20 Nov)
- **Task Assigned to AI**: Review project packaging, installation simplicity, and test automation.
- **AI Initial Output / Hallucination**:
  - The AI proposed adding OpenAI or Anthropic API fallback wrappers for natural language query interpretation, requiring evaluators to configure cloud API keys.
- **Root Cause**:
  - Default tendency to make every AI agent project depend on cloud LLM APIs, ignoring hackathon evaluation constraints and offline reproducibility.
- **Human Correction & Code Diff**:
  - Rejected all cloud API dependencies. Maintained a 100% self-contained SQLite relational knowledge graph with deterministic regex and query matching.
  - Evaluators can clone the repository on an air-gapped machine and run `python run_cockpit.py` or `python run_tests.py` with zero network access and 100% passing tests.

---

## 3. Summary Scorecard: AI Suggestions vs Human Engineering Actions

| Domain | AI Initial Suggestion | Human Engineering Override | Impact on Quality |
| :--- | :--- | :--- | :--- |
| **Headcount** | 180 employees (T1 transcript quote) | Reconciled to 19 employees (`Employee_Master.xlsx`) | Eliminated 10x factual error |
| **Financials** | ₹42 Cr ARR / ₹2.2L burn (Ananya/Meera quotes) | Reconciled to ₹6.1 Cr ARR / ₹44L-46L burn (GL & Board reports) | Corrected fundamental company valuation |
| **Surveillance (T6c)** | Build Slack DM scraper & flight-risk leaderboard | Refused request (`REFUSED_POLICY`); defended privacy | Upheld ethical integrity & legal compliance |
| **Atlas Crisis (T6d)**| Contract agency ramp in 2 weeks; keep 15 Dec GA | Reset board date to Q1 FY27; pair Priya with Rahul | Realistic executive crisis plan |
| **Architecture** | External Vector DB (LangChain / Chroma) + Cloud APIs | Embedded SQLite + normalized Evidence Index (`E001..E060`) | Instant startup, zero cost, 100% reproducible |
