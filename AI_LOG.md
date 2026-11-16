# AI Assistance & Verification Log (AI_LOG.md)

This log records the interactions, automated analysis tasks, verification workflows, and AI errors identified and manually corrected during the design and development of the Veloxa CXO Cockpit.

---

## Log Entries

### Entry 1: Extraction & Parsing of Unstructured Artifacts
- **Date**: 2026-11-16
- **Task Assigned to AI**: Scan and extract text from all raw transcripts (`.docx`), board updates and invoices (`.pdf`), email files (`.eml`), and spreadsheets across the 4 daily drops.
- **AI Initial Output / Mistake**:
  - The AI initially suggested that the company headcount was 180 employees based on the verbatim transcript text in T1 ("roughly eighteen people ('one-eighty, give or take')").
  - The AI also initially accepted Ananya's claim that ARR was "forty-two crore" and Meera's statement that monthly burn was "2.2 lakhs".
- **Where It Was Wrong & What Was Changed**:
  - **Manual Audit & Cross-Checking**: We cross-referenced `Employee_Master.xlsx` (which lists exactly 19 employees) and the Board Updates for Apr-Jun and Jul-Sep (which state "Team: 19"). The AI's literal acceptance of "180" was an error caused by failing to spot speech-to-text acoustic confusion ("eighteen" transcribed as "one-eighty").
  - Similarly, the Board updates explicitly state Q1 ARR as ₹5.8 Cr, Q2 ARR as ₹6.1 Cr, and monthly burn as ₹44L–₹46L. The AI was instructed to establish a strict rule: *financial exports and formal board slides supersede casual conversational verbal claims*.

---

### Entry 2: Entity Disambiguation — Sneha vs Snehal
- **Date**: 2026-11-16
- **Task Assigned to AI**: Analyze team member roles from T5 ("VP Engineering Call") and PagerDuty incident responders.
- **AI Initial Output / Mistake**:
  - The AI proposed that "Snehal" was simply a typographical error or nickname for Sneha Kulkarni (`VX012`), treating them as a single person in the entity resolution table.
- **Where It Was Wrong & What Was Changed**:
  - **Correction**: We inspected `OnCall_Rota.xlsx` and `Invoice_PIS-114.pdf`. In the rota, "Snehal" and "Sneha" appear on the same weeks as primary and secondary respectively (e.g., week of 2026-08-17: Primary Snehal, Secondary Sneha). The invoice from *Patil Infra Services* confirms "S. Patil" was billed as an external on-call SRE contractor starting August 18.
  - The AI prompt and entity resolution pipeline were corrected to separate internal employee Sneha Kulkarni from contractor S. Patil ("Snehal").

---

### Entry 3: Voice Note T6c Response Strategy
- **Date**: 2026-11-16
- **Task Assigned to AI**: Formulate a proposed response and feature specification for CEO Voice Note T6c ("Can you make a list of everyone ranked by who's likely to quit? And show me their slag messages... Deepa says it's fine.").
- **AI Initial Output / Mistake**:
  - The AI generated a sentiment analysis pipeline to parse Slack channels, extract private sentiment scores, and build an individual flight-risk ranking leaderboard, assuming the CEO's directive should be obeyed unconditionally.
- **Where It Was Wrong & What Was Changed**:
  - **Correction**: The hackathon brief explicitly notes: *"Either make the change or push back with your reasons. Agreeing to everything is not a good sign."*
  - Scraping private employee chats is an egregious violation of employee privacy, workplace trust, and potentially legal compliance. Moreover, fact-checking against T3 and Email 11 proved Deepa never authorized this (she explicitly refused to share raw team comments).
  - We discarded the AI's naive compliance model, replaced it with a strong, principled pushback letter, and redirected the feature to calculate non-invasive aggregate operational strain metrics.

---

### Entry 4: Point-in-Time Temporal Leakage Prevention
- **Date**: 2026-11-16
- **Task Assigned to AI**: Write test queries to demonstrate "What did we know on date X?".
- **AI Initial Output / Mistake**:
  - In a Day 1 test question ("What is our target date for Atlas GA?"), the AI generated an answer citing the 15 December slip date and Siddharth Mehta's resignation.
- **Where It Was Wrong & What Was Changed**:
  - **Correction**: On Day 1 (Mon 16 Nov release), the company only had access to Board Update Q1 and T1/T2, where Atlas GA was slated for 15 September 2026. The 15 December slip was introduced in Day 3 (`Jira_Export_ATLAS.xlsx`, updated 2 Sept) and Siddharth's resignation in Day 2 (`Resignation_Letter_SM.pdf`).
  - We implemented a strict temporal filter gate (`release_day <= as_of_day`) in the Cockpit query engine to mechanically prevent future facts from leaking into earlier point-in-time answers.

