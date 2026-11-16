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
