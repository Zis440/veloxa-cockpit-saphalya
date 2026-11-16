# Veloxa CXO Cockpit

An executive intelligence tool built for Veloxa Technologies CEO Ananya Rao. The system reconciles disparate, conflicting records across 4 drops of data room exports (HRMS, Zoho Books GL, Jira, GitHub logs, PagerDuty, emails) and machine-transcribed leadership calls.

**Author**: Saphalya (`veloxa-cockpit-saphalya`)  
**Hackathon**: Hiyaku Systems Hackathon 2026  

---

## 1. Quickstart (One-Command Run)

### Run the Interactive CLI Cockpit:
```bash
python run_cockpit.py
```
*Immediately displays the **Top 3 What to Worry About** executive risks on startup (satisfying CEO Voice Note T6a), lets you query the oracle, interview colleagues, and shift temporal release dates (`day 1` to `day 4`).*

### Run the Executive Web Dashboard:
```bash
python run_cockpit.py --web
```
*Opens an interactive web dashboard on **http://localhost:5000** with dynamic risk cards, point-in-time slider, 1:1 agent interview chat room, and post-Oct 31 simulation timeline.*

### Run the Automated Test Suite (25 Tests):
```bash
python run_cockpit.py --test
# or
python run_tests.py
```
*Executes all **25 automated tests** across epistemic refusals, temporal non-leakage, fact verification, persona interviews, and stretch goal simulation.*

---

## 2. Core Capabilities

- **Direct Citations**: Answers executive questions with exact references to data room records (`[Ref E042: git_log.csv]`, `[Ref E040: Jira_Export_ATLAS.xlsx]`).
- **Epistemic Refusal**: Explicitly reports *"I don't know: no records in the data room cover this topic"* or *"The sources disagree"* when data is missing or contradictory.
- **Strict Temporal Isolation**: Supports `as_of_day` (Day 1 through Day 4) preventing future information from leaking into earlier queries.
- **Top 3 What to Worry About**: Automated operational risk cards dynamically ranked by severity and backed by records.
- **14 Grounded Colleague Personas**: Real interactive agents across Engineering, Finance, HR, and Marketing reflecting true workload, commit counts, tickets, and psychological state.
- **Post-Oct 31 Autonomous Simulation (Stretch Goal)**: Discrete-event engine generating realistic daily activity (commits, handover pairing, on-call shifts) past 31 October 2026.
- **Principled Responses to CEO Voice Notes**: Written responses to T6a, T6b, T6c (**firm ethical pushback refusing Slack surveillance**), and T6d (Atlas crisis plan).

---

## 3. Project Structure

```text
├── ARCHITECTURE.md            # System architecture, SQLite schema, and design rationale
├── TRANSCRIPT_NOTES.md        # Audit of transcription errors, mishearings, and contradictions
├── ASSUMPTIONS.md             # Assumption register with source lines and confidence ratings
├── DECISIONS.md               # Architecture Decision Records (ADRs)
├── VOICE_NOTE_RESPONSES.md    # Formal written responses to CEO voice notes (T6a–T6d)
├── AI_LOG.md                  # Honest log of AI assistance, hallucinations caught, and manual fixes
├── run_cockpit.py             # One-command CLI and Web dashboard launcher
├── run_tests.py               # 25-question automated verification test suite
├── veloxa_cockpit.db          # Self-contained SQLite relational database
├── reconciled_worksheets/     # Exported Entity_Resolution.xlsx and Evidence_Index.xlsx
└── src/
    ├── models.py              # SQLite schema definition (16 tables)
    ├── ingestion.py           # Multi-modal parsing and reconciliation pipeline
    ├── evidence.py            # Evidence Index (E001..E060) and Entity Resolution mappings
    ├── cockpit_engine.py      # Query oracle, temporal filter, refusal gate, Top 3 risk ranker
    ├── agents.py              # 14 Grounded Personas and 1:1 interview engine
    ├── simulation.py          # Autonomous post-Oct 31 daily event generator
    └── web_dashboard.py       # Flask web application
```

---

## 4. Key Contradictions Resolved

1. **Company Size**: Ananya's verbal statement of *"one-eighty, give or take"* in T1 was an acoustic speech-to-text mishearing of *"eighteen"*. Ground truth is **19 active employees** (`Employee_Master.xlsx`, Board Reports).
2. **ARR & Burn Rate**: Ananya's claim of *"around forty-two crore"* ARR and Meera's *"2.2 lakhs"* burn in T1/T2 conflict with official financial records. Ground truth is **₹6.1 Cr ARR** and **₹44L–₹46L monthly burn** (`Board_Update_Jul-Sep_2026.pdf`, `GL_Export_Apr-Sep_2026.xlsx`).
3. **Sneha vs. Snehal**: Sneha Kulkarni (`VX012`) is the internal full-time SRE employee. "Snehal" is **S. Patil**, an external contractor from *Patil Infra Services* (Invoice `PIS-114`) hired in August to relieve on-call pressure.
4. **Atlas v3 Delivery**: Vikram quietly pushed Atlas GA in Jira from 15 Sep to 15 Dec 2026 on 2 Sept (`Jira_Export_ATLAS.xlsx`). Priya Nair's subsequent resignation on 19 Nov (Voice note T6d) renders 15 Dec unachievable, requiring a reset to Q1 FY27.
5. **Ethical Refusal (T6c)**: The cockpit firmly refuses Ananya's request to read employee private Slack messages. Deepa never approved this; doing so violates privacy laws and employee trust.
