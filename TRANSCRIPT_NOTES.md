# Transcript Notes & Reconciliations

This document logs all suspected mishearings, factual discrepancies, machine-transcription errors, and contradictions between the auto-generated call transcripts and the ground-truth system exports across Veloxa's data room.

---

## 1. Machine-Transcription Mishearings & Phonetic Resolutions

| Transcript & Speaker | Phrase / Identifier in Transcript | Resolved Entity / Term | Evidence & Cross-Reference | Resolution & Impact |
| :--- | :--- | :--- | :--- | :--- |
| **T1 (CEO)** | "one-eighty, give or take" (Company size) | **19 employees** (approx. 18-19) | `Employee_Master.xlsx`: 19 rows; `Board_Update_Apr-Jun_2026.pdf`: Team: 19; `Board_Update_Jul-Sep_2026.pdf`: Team: 19. | Auto-transcription misheard "eighteen" as "one-eighty". Veloxa is an 18-to-19 person company, not 180. |
| **T1 (CEO)** | "around forty-two crore, maybe forty-five now" | **₹4.2 - ₹4.5 Cr ARR** (or confusion with valuation) | Board reports: Q1 ARR ₹5.8 Cr, Q2 ARR ₹6.1 Cr. CFO Meera in T2 states "forty-eight" (₹4.8 Cr). | Ananya's "forty-two crore" was a verbal slip or transcription error for "4.2 to 4.5 crore", or she quoted an ungrounded valuation figure. Ground truth is ₹5.8 Cr – ₹6.1 Cr. |
| **T1 (CEO)** | "Linear, I think, or they moved back to the Jeera board" | **Jira** (Project ATLAS) | `Jira_Export_ATLAS.xlsx`, T5 VP Eng call ("we tried Linear for a month and went back"). | Phonetic error for Atlassian Jira. Project ATLAS is actively managed in Jira. |
| **T1 (CEO)** | "Pria basically holds the routing thing together" | **Priya Nair** (`VX007`) | `Employee_Master.xlsx` (Staff Engineer), `git_log.csv` (425 commits from `priya.n@veloxa.in`, 163 from `pnair@users.noreply.github.com`). | Machine spelling "Pria" resolved to Staff Engineer Priya Nair, lead of core routing engine. |
| **T1 (Action Items)** | "Send the hub sport export" | **HubSpot** | `T4_Head_of_Marketing_Call.docx` ("Leads tracked in Hub Spot"). | Phonetic mishearing of HubSpot CRM. |
| **T1 (Action Items)**, **T6c (CEO)** | "slag channel", "show me their slag messages" | **Slack** | Internal messaging tool Slack. | Machine transcription phonetically parsed "Slack" as "slag". |
| **T2 (CFO)** | "April to March, so we're in FY twenty-six" (note: may have said twenty-seven) | **FY 2026-27** (or FY27) | `GL_Export_Apr-Sep_2026.xlsx` covers transactions from April 2026 to Sept 2026. | Indian fiscal year running April 2026 – March 2027 is conventionally designated FY 2026-27 or FY27. |
| **T2 (CFO)** | "two point two lakhs a month, sometimes two point five" | **₹44L - ₹46L monthly burn** (or misheard 42-45L) | `Board_Update_Apr-Jun_2026.pdf` (Burn: Rs. 46 L), `Board_Update_Jul-Sep_2026.pdf` (Burn: Rs. 44 L), `Payroll_Register_Jan-Mar_2026.xlsx` (monthly payroll alone is ₹31.75L). | CFO's statement of "2.2 lakhs" is mathematically impossible with a ₹31.75L monthly payroll. Either speaker said "forty-two lakhs" or was referring to non-payroll discretionary burn. Ground truth burn is ₹44L-₹46L. |
| **T2 (CFO)** | "Joho books" | **Zoho Books** | `GL_Export_Apr-Sep_2026.xlsx` ("General ledger export, Zoho Books"). | Phonetic mishearing of Zoho Books. |
| **T2 (CFO)**, **T3 (People)** | "Kayka", "Kekka" | **Keka HRMS** | `Employee_Master.xlsx`, `Hiring_Tracker.xlsx` ("Keka HRMS export"). | Phonetic mishearing of Keka. |
| **T3 (People)** | "Cult Amp" | **Culture Amp** | `Pulse_Survey.xlsx` ("Culture Amp quarterly pulse"). | Phonetic mishearing of Culture Amp employee feedback tool. |
| **T3 (People)** | "Hiring runs on Liver" | **Lever ATS** | `Hiring_Tracker.xlsx`, recruiter terminology. | Phonetic mishearing of Lever Applicant Tracking System. |
| **T5 (VP Eng)** | "incidents in August that pulled Snehal off... Sneha later" | **Sneha Kulkarni** (Employee) vs **Snehal / S. Patil** (Contractor) | `Employee_Master.xlsx` (Sneha Kulkarni `VX012`); `Invoice_PIS-114.pdf` (S. Patil, Patil Infra Services); `OnCall_Rota.xlsx` (primary shifts swapped between Sneha and Snehal in late Aug). | **Crucial entity distinction**: Sneha Kulkarni is the internal full-time SRE. "Snehal" is S. Patil, an external DevOps contractor hired on 18 Aug 2026 to offload on-call duties. |

---

## 2. Cross-Source Contradictions & Reconciled Truth

### Contradiction 1: Engineering Velocity vs Atlas v3 Release Date
- **Transcripts**:
  - T1 (CEO): Promised to customers "by the festive season" (Oct/Nov).
  - T5 (VP Eng Vikram): "on track, maybe a couple of weeks buffer... Board date is still September-ish... everyone's busy, that's startups".
- **Exports & Documents**:
  - `Jira_Export_ATLAS.xlsx` (Versions tab): Original Release Date: `2026-09-15`. Release Date: `2026-12-15`. Last Changed: `2026-09-02` by `vikram`.
  - `Email 04` (Vikram to Ananya, 2 Jun): "15 Sep GA is achievable if the two backend hires land by July."
  - `Email 06` (Meera to Vikram, 12 Aug): Pausing REQ-014 and REQ-015 (backend engineers) to protect burn.
  - `Email 08` (Sneha to Vikram, 24 Aug): Third SEV1 this month; pausing Atlas perf tickets to stabilize routing-api.
  - `Incidents_Aug-Oct_2026.xlsx`: 3 major SEV1 incidents in August on `routing-api` (INC-201, INC-203, INC-205) each taking 3 to 6+ hours to resolve.
- **Reconciliation & Verdict**:
  - Vikram has systematically downplayed delays to Ananya. Atlas was secretly slipped to **15 December 2026** in Jira on September 2, 2026.
  - The prerequisites for the September 15 date (the 2 backend hires) were cancelled in mid-August by Meera. The platform suffered 3 SEV1 outages that completely diverted Sneha. Atlas is at extreme delivery risk.

### Contradiction 2: Marketing Summit Pipeline & Spend
- **Transcripts**:
  - T4 (Nikhil): September summit was "our best quarter ever for pipeline". Marketing spend for the half was "1.8" by his numbers. Dismisses Manoj's feedback that leads are cold.
- **Exports & Documents**:
  - `Board_Update_Jul-Sep_2026.pdf`: Logistics Summit drew 212 registrations.
  - `GL_Export_Apr-Sep_2026.xlsx`:
    - Google Ads (MKT-PS): ~₹76K - ₹84K/month (~₹4.8L total)
    - Event Venue & Production (MKT-EV, JV-0925): ₹11,80,000
    - Collateral & Design (MKT-EV, JV-0914): ₹2,10,000
    - Total recorded H1 marketing spend in GL = ₹24,10,000 (₹24.1 Lakhs).
- **Reconciliation & Verdict**:
  - When Nikhil claims spend was "one point eight", he likely meant ₹18 Lakhs (excluding digital ad run-rate) or ₹1.8 million ($22K). Finance's books show ₹24.1 Lakhs total.
  - In addition, sales lead Manoj notes summit leads are low-intent / cold, meaning the pipeline conversion claim is unvalidated vanity metrics.

### Contradiction 3: Feb 2026 Payroll Overpayment
- **Emails**:
  - `01.eml` (Karthik to Meera, 28 Feb): Karthik ran payroll using January sheet while Fatima was on leave. Added the new joiner.
  - `02.eml` (Rahul Verma to Fatima, 6 Mar): Rahul noticed his first paycheck was higher than expected for a partial month. Joined Feb 3.
  - `03.eml` (Fatima to Rahul, 10 Mar): "Will check and get back."
- **Exports**:
  - `Payroll_Register_Jan-Mar_2026.xlsx`: Rahul Verma (`VX018`) was paid for 28 Days Payable in Feb (Gross ₹1,50,000, Net ₹1,32,000), exactly equal to a full 28-day month instead of deducting the days prior to his joining date (Feb 3) or proration adjustments.
- **Reconciliation & Verdict**:
  - Karthik made an unprorated payroll run. Rahul Verma honestly flagged the overpayment, but finance never clawed it back or adjusted it in March payroll records.

### Contradiction 4: Siddharth Mehta's Resignation Reason
- **Transcripts**:
  - T3 (Deepa): Mentions "Sid from marketing has put in his papers" and says exit interviews cite "workload".
- **Documents**:
  - `Resignation_Letter_SM.pdf` (Siddharth Mehta, 15 Sept 2026): "I'm looking for a role with clearer launch timelines, where the work I prepare reaches customers. I'll hand over everything I've built, including the launch kit, before I leave."
  - `Atlas_Launch_Kit_v1.pdf`: Completed on 21 July 2026, sitting idle for months due to engineering slips.
- **Reconciliation & Verdict**:
  - Deepa's blanket claim of "workload" obscures the true reason: product marketing demoralization caused by repeated engineering launch delays.

