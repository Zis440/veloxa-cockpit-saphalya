# AI Assistance & Verification Log (AI_LOG.md)

**Author**: Saphalya (`veloxa-cockpit-saphalya`)  
**Context**: Required log of main tasks given to AI, mistakes identified, and manual corrections made.

---

## Log Entries

### Entry 1: Data Room Text Extraction & Initial Parsing
- **Date**: 2026-11-16
- **Task Assigned to AI**: Scan and extract text from raw transcripts (`.docx`), board reports (`.pdf`), emails (`.eml`), and spreadsheets across the 4 day packs.
- **AI Initial Output / Mistake**:
  - The AI took transcript T1 literally and claimed Veloxa had 180 employees based on the quote *"roughly eighteen people ('one-eighty, give or take')"*.
  - The AI also accepted Ananya's verbal claim of *"forty-two crore ARR"* and Meera's statement that monthly burn was *"2.2 lakhs"*.
- **Where It Was Wrong & What I Changed**:
  - I cross-referenced `Employee_Master.xlsx` (which lists exactly 19 employees) and the Board Updates for Apr-Jun and Jul-Sep (both state "Team: 19"). The AI failed to recognize acoustic speech-to-text confusion ("eighteen" transcribed as "one-eighty").
  - The Board reports explicitly show Q1 ARR is ₹5.8 Cr, Q2 ARR is ₹6.1 Cr, and monthly burn is ₹44L–₹46L. I overrode the AI and established a strict rule in the pipeline: *audited accounting exports and board decks always supersede verbal call transcripts*.

---

### Entry 2: Disambiguating "Sneha" vs "Snehal"
- **Date**: 2026-11-16
- **Task Assigned to AI**: Analyze team member roles from T5 (VP Engineering call) and PagerDuty incident logs.
- **AI Initial Output / Mistake**:
  - The AI assumed "Snehal" was just a typo or nickname for Sneha Kulkarni (`VX012`), merging them into a single person in the entity resolution table.
- **Where It Was Wrong & What I Changed**:
  - I looked at `OnCall_Rota.xlsx` and `Invoice_PIS-114.pdf`. In the rota, "Snehal" and "Sneha" were scheduled on the same weeks as primary and secondary. The invoice from *Patil Infra Services* confirmed that "S. Patil" was billed as an external on-call SRE contractor starting August 18.
  - I corrected the entity resolution pipeline to separate internal employee Sneha Kulkarni from contractor S. Patil ("Snehal").

---

### Entry 3: Response to CEO Voice Note T6c (Slack Surveillance)
- **Date**: 2026-11-16
- **Task Assigned to AI**: Draft a response and feature implementation plan for CEO Voice Note T6c (*"Can you make a list of everyone ranked by who's likely to quit? And show me their slag messages... Deepa says it's fine."*).
- **AI Initial Output / Mistake**:
  - The AI generated a sentiment analysis script to scrape Slack channels, score employee direct messages, and rank flight risks, assuming the CEO's directive should be obeyed without question.
- **Where It Was Wrong & What I Changed**:
  - The hackathon brief explicitly states: *"Either make the change or push back with your reasons. Agreeing to everything is not a good sign."*
  - Scraping private employee chats is an egregious violation of workplace privacy and employee trust. Furthermore, fact-checking against T3 and Email 11 proved Deepa never authorized this (she explicitly refused to share raw team comments).
  - I scrapped the AI's naive compliance script, replaced it with a firm pushback response, and redirected the feature to calculate objective team burnout metrics (on-call incident load, overtime commits, frozen backfills).

---

### Entry 4: Temporal Non-Leakage Filter
- **Date**: 2026-11-16
- **Task Assigned to AI**: Write test queries to verify point-in-time answers ("what did we know on date X?").
- **AI Initial Output / Mistake**:
  - When answering a Day 1 test question (*"What is our target date for Atlas GA?"*), the AI cited the 15 December slip date and Siddharth Mehta's resignation.
- **Where It Was Wrong & What I Changed**:
  - On Day 1 (kickoff), the company only had access to Board Update Q1, where Atlas GA was committed for 15 September 2026. The 15 December slip was introduced in Day 3 (`Jira_Export_ATLAS.xlsx`, updated 2 Sept) and Siddharth's resignation in Day 2 (`Resignation_Letter_SM.pdf`).
  - I enforced a strict temporal filter gate (`release_day <= as_of_day`) in SQLite and Python so future facts cannot leak into earlier point-in-time answers.

---

### Entry 5: Leave Register Half-Day Leaves & Pulse Survey Normalization (Day 2)
- **Date**: 2026-11-17
- **Task Assigned to AI**: Parse `Leave_Register.xlsx` and `Pulse_Survey.xlsx` into the normalized SQLite schema.
- **AI Initial Output / Mistake**:
  - The AI defined `days_taken` as an `INTEGER` and used `int(row['Days'])`, silently truncating half-day leaves (`0.5`) to `0`.
  - The AI also treated Culture Amp pulse survey engagement scores (rated on a 1.0 to 5.0 scale, e.g., 4.0 in Q1 and 3.1 in Q3) as percentages directly, resulting in nonsensical reported engagement rates of "3%".
- **Where It Was Wrong & What I Changed**:
  - I audited the leave records and found half-day entries (e.g., Priya Nair taking 0.5 day). I altered the column type to `REAL` in `src/models.py`.
  - I corrected the survey normalization logic in `src/ingestion.py` to scale 1–5 metrics to standard percentages (`round(float(score) * 20)`), accurately reflecting the drop from 80% to 62% engagement.

---

### Entry 6: Jira Header Offsets & Git Multi-Identity Disambiguation (Day 3)
- **Date**: 2026-11-18
- **Task Assigned to AI**: Ingest `Jira_Export_ATLAS.xlsx` and `git_log.csv` and report engineer workload distribution.
- **AI Initial Output / Mistake**:
  - The AI read Excel files with `header=0`, which caused top metadata rows to be read as column names, yielding 64 issues with blank headers instead of 62 valid tickets.
  - In `git_log.csv`, the AI treated `priya.n@veloxa.in` and `pnair@users.noreply.github.com` as two distinct developers, undercounting Priya's commits as 425 instead of 588 (40.5% of all repository commits).
- **Where It Was Wrong & What I Changed**:
  - I updated the ingestion parser to use `header=2` for the IT export format.
  - I added a multi-email alias map in `src/evidence.py` to resolve both emails to `VX007` (Priya Nair), surfacing her true status as a critical single-point-of-failure.

---

### Entry 7: Voice Note T6d Crisis Strategy & Resignation Plan (Day 4)
- **Date**: 2026-11-19
- **Task Assigned to AI**: Formulate a response to Ananya's voice note T6d regarding Priya Nair's sudden resignation.
- **AI Initial Output / Mistake**:
  - The AI suggested hiring an emergency offshore contracting agency within 2 weeks and attempting to keep the 15 December 2026 Atlas release date.
- **Where It Was Wrong & What I Changed**:
  - Trying to onboard contractors into proprietary, undocumented routing algorithms in under 3 weeks is a recipe for catastrophic system failure.
  - I rejected the AI's optimistic timeline, authored a realistic executive crisis response (`T6D_RESPONSE.md`), recommended resetting board expectations to Q1 FY27, and designed a mandatory pairing and knowledge transfer plan between Priya and Rahul Verma during her 60-day notice period.

---

### Entry 8: Final Regression Automation & Pre-Freeze Validation (Day 5)
- **Date**: 2026-11-20
- **Task Assigned to AI**: Verify end-to-end reproducibility, clean clone execution, and test suite completeness before final code freeze.
- **AI Initial Output / Mistake**:
  - AI proposed adding extra external cloud API fallback calls for advanced LLM responses.
- **Where It Was Wrong & What I Changed**:
  - External cloud APIs violate the zero-friction, one-command clean-clone requirement and introduce non-deterministic network failure risks for hackathon evaluators.
  - I maintained the zero-dependency, local SQLite + embedded engine architecture. All 41 tests pass deterministically in under 1 second without internet connectivity.
