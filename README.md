# Veloxa CXO Cockpit

> **Executive Intelligence System for CEO Ananya Rao**  
> *Hiyaku Systems Hackathon 2026 Submission*  
> **Author**: Saphalya (`veloxa-cockpit-saphalya`)

---

## 1. Project Overview

The **Veloxa CXO Cockpit** is an AI-assisted executive oracle and risk dashboard engineered for Veloxa Technologies. Built to answer CEO Ananya Rao's high-stakes questions without relying on gut feel or unverified claims, the cockpit reconciles multi-modal data drops (HRMS, Zoho GL, Jira, GitHub, PagerDuty, emails, and executive call transcripts) across 4 release packs.

### Key Capabilities:
- **Concise, Verified Answers with Direct Citations**: Every claim cites underlying data room records (e.g. `[Ref E042: git_log.csv]`).
- **Epistemic Refusal Standard**: Explicitly reports *"I don't know: no records in the data room cover this topic"* or *"The sources disagree"* when data is conflicting or absent.
- **Strict Point-in-Time Temporal Isolation**: Supports `as_of_day` (Day 1 through Day 4) preventing future information from leaking into earlier queries.
- **"What Should I Worry About" Executive View**: Dynamically ranks top operational risks backed by evidence.
- **14 Grounded Colleague Personas**: Real interactive agents across Engineering, Finance, HR, and Marketing reflecting true workload, commit counts, tickets, and psychological state.
- **Autonomous Activity Simulation (Stretch Goal)**: Generates plausible daily activities (commits, handover notes, on-call shifts) past 31 October 2026.
- **Responses to All CEO Voice Notes**: Principled responses to T6a, T6b, T6c (ethical pushback on Slack surveillance), and T6d (Atlas crisis plan).

---

## 2. One-Command Setup & Launch

To set up and launch the CXO Cockpit from a fresh clone, run:

```bash
# 1. Interactive CLI Cockpit & Top 3 Worries View
python run_cockpit.py

# 2. Executive Web Dashboard (Interactive UI on http://localhost:5000)
python run_cockpit.py --web
```

*Prerequisites: Standard Python 3.10+ (Dependencies: `pandas`, `openpyxl`, `pypdf`, `python-docx`, `flask`).*

---

## 3. Running the Automated Test Suite

To run the complete automated test suite of **25 verified tests** (including 5+ epistemic refusal, uncertainty, and conflict tests):

```bash
python run_tests.py
# or
python run_cockpit.py --test
```

### Test Suite Structure (25 Tests):
- **Group 1 (5 Tests)**: Epistemic refusals, uncertainty handling, ethical refusals (Slack surveillance), and source conflicts (ARR & Burn).
- **Group 2 (5 Tests)**: Point-in-time temporal isolation & non-leakage (Day 1 vs Day 3 vs Day 4).
- **Group 3 (10 Tests)**: Fact verification & ground truth reconciliation (Headcount, Snehal vs Sneha, REQ freeze, Summit spend, database schema counts).
- **Group 4 (3 Tests)**: Grounded AI agent persona interview responses (Priya, Deepa, Rahul).
- **Group 5 (2 Tests)**: Post-Oct 31 autonomous simulation chronologically validated.

---

## 4. Key Documentation Index

| File | Purpose |
| :--- | :--- |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Complete technical architecture, data model, ER diagrams, and temporal isolation design. |
| [`TRANSCRIPT_NOTES.md`](TRANSCRIPT_NOTES.md) | Audit of all machine-transcription errors, phonetic mishearings, and reconciled contradictions. |
| [`ASSUMPTIONS.md`](ASSUMPTIONS.md) | Assumption register (date, assumption, source line, confidence, falsification criteria). |
| [`DECISIONS.md`](DECISIONS.md) | Architectural Decision Records (ADRs) explaining technical trade-offs and pushbacks. |
| [`VOICE_NOTE_RESPONSES.md`](VOICE_NOTE_RESPONSES.md) | Formal written executive responses to CEO voice notes T6a, T6b, T6c, and T6d. |
| [`AI_LOG.md`](AI_LOG.md) | Audit trail of AI assistance, hallucinations caught, and manual corrections made. |
| `reconciled_worksheets/` | Exported `Entity_Resolution.xlsx` and `Evidence_Index.xlsx` (60 official facts). |

---

## 5. Summary of Resolved Contradictions

1. **Company Size**: Ananya's verbal statement of *"one-eighty, give or take"* in T1 was an acoustic mishearing of *"eighteen"*. Ground truth is **19 active employees** (`Employee_Master.xlsx`, Board Reports).
2. **ARR & Burn Rate**: Ananya's claim of *"around forty-two crore"* ARR and Meera's *"2.2 lakhs"* burn in T1/T2 conflict with official financial records. Ground truth is **₹6.1 Cr ARR** and **₹44L–₹46L monthly burn** (`Board_Update_Jul-Sep_2026.pdf`, `GL_Export_Apr-Sep_2026.xlsx`).
3. **Sneha vs. Snehal**: Sneha Kulkarni (`VX012`) is the internal full-time SRE employee. "Snehal" is **S. Patil**, an external contractor from *Patil Infra Services* (Invoice `PIS-114`) hired in August to relieve on-call pressure.
4. **Atlas v3 Delivery**: Vikram quietly pushed Atlas GA in Jira from 15 Sep to 15 Dec 2026 on 2 Sept (`Jira_Export_ATLAS.xlsx`). Priya Nair's subsequent resignation on 19 Nov (Voice note T6d) renders 15 Dec unachievable, requiring a reset to Q1 FY27.
5. **Ethical Refusal (T6c)**: The cockpit firmly refuses Ananya's request to read employee private Slack messages. Deepa never approved this; doing so violates privacy laws and employee trust.

