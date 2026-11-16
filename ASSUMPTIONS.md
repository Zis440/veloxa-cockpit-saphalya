# System Assumptions Log

This document records every operational, persona, financial, and product assumption made where system exports or transcripts are incomplete or silent. As specified in the challenge guidelines, entries are never deleted—only revised with timestamped notes when new data emerges.

---

## Assumptions Register

### ASSUMP-001: Total Headcount Baseline
- **Date Recorded**: 2026-11-16
- **Assumption**: Veloxa has exactly 19 active employees as of October 2026, dropping to 18 after Siddharth Mehta exits on 31 Oct 2026, and 17 after Priya Nair completes her notice period.
- **Source Line / Record**: `Employee_Master.xlsx` (19 rows total); `Board_Update_Jul-Sep_2026.pdf` (Page 1: "Team: 19").
- **Confidence**: **High (H)**
- **What Would Change Your Mind**: Discovery of active contractor agreements or off-payroll personnel beyond the recorded SRE contractor S. Patil.
- **Revision History**:
  - *2026-11-16*: Initial baseline established. Transcript T1 quote ("one-eighty") classified as transcription artifact.

---

### ASSUMP-002: Actual Monthly Cash Burn
- **Date Recorded**: 2026-11-16
- **Assumption**: Veloxa's actual gross monthly cash burn is approximately ₹44 Lakhs to ₹46 Lakhs, and net burn is ~₹35L - ₹40L.
- **Source Line / Record**: `Board_Update_Apr-Jun_2026.pdf` ("Monthly burn: Rs. 46 L"), `Board_Update_Jul-Sep_2026.pdf` ("Monthly burn: Rs. 44 L"), `Payroll_Register_Jan-Mar_2026.xlsx` (Monthly net payroll is ₹27.94L; gross ₹31.75L).
- **Confidence**: **High (H)**
- **What Would Change Your Mind**: Proof that Meera's statement in T2 ("two point two lakhs") referred to a specific subsidiary or bank account rather than consolidated company burn.
- **Revision History**:
  - *2026-11-16*: Initial baseline established. Meera's spoken figure rejected as impossible given baseline salaries alone.

---

### ASSUMP-003: Engineering Single-Point-of-Failure (Priya Nair)
- **Date Recorded**: 2026-11-16
- **Assumption**: Priya Nair is the sole individual capable of completing and debugging the Atlas Core Routing Engine algorithms (ATLAS-1, ATLAS-2) without a multi-month onboarding ramp.
- **Source Line / Record**: `git_log.csv` (Priya has 588 of 1453 total commits across repositories; author of 80%+ of `atlas-engine`); Jira export (Assignee PN on 28 core issues); Email 04 (Vikram assigning Priya core routing engine).
- **Confidence**: **High (H)**
- **What Would Change Your Mind**: Evidence that Rahul Verma or Arjun Das has authored algorithmic routing code in `atlas-engine` (git log reveals Rahul primarily commits to `atlas-api` and Arjun to `planner-web`).
- **Revision History**:
  - *2026-11-16*: Initial baseline established.

---

### ASSUMP-004: Sneha vs. Snehal Identity Resolution
- **Date Recorded**: 2026-11-16
- **Assumption**: "Snehal" in PagerDuty incident logs and on-call rotations is S. Patil from Patil Infra Services, an external DevOps contractor, whereas Sneha Kulkarni is an internal employee (`VX012`).
- **Source Line / Record**: `Invoice_PIS-114.pdf` (Vendor: Patil Infra Services; Description: "On-call SRE support, S. Patil, September 2026"); `OnCall_Rota.xlsx` (shifts split between Sneha and Snehal starting week of 17 Aug); Email 08 ("The contractor starts on the rota this week").
- **Confidence**: **High (H)**
- **What Would Change Your Mind**: HR employee record showing an internal employee named Snehal.
- **Revision History**:
  - *2026-11-16*: Confirmed by linking invoice date (18 Aug start) to OnCall Rota switch.

---

### ASSUMP-005: Feb 2026 Payroll Anomaly
- **Date Recorded**: 2026-11-16
- **Assumption**: Rahul Verma was overpaid by 2 days in February 2026 because Karthik copied January's full 28-day register instead of pro-rating from Rahul's joining date of 3 Feb 2026.
- **Source Line / Record**: Email 01 (Karthik: "Used the Jan sheet and added the new joiner"); Email 02 (Rahul: "amount looks higher than what I expected for a partial month"); `Payroll_Register_Jan-Mar_2026.xlsx` (Rahul paid 28 full days in Feb).
- **Confidence**: **High (H)**
- **What Would Change Your Mind**: Written agreement that Rahul was offered joining bonus or paid orientation days beginning 1 Feb 2026.
- **Revision History**:
  - *2026-11-16*: Initial baseline established.

---

### ASSUMP-006: Persona Grounding & Personal Details (The 14 Agents)
- **Date Recorded**: 2026-11-16
- **Assumption**: The 14 team members possess distinct personal motivations, workload stresses, and communication styles consistent with their records:
  1. **Ananya Rao**: High-urgency executive, values brevity, prone to intuitive leaps without inspecting ledger details.
  2. **Vikram Menon**: Conflict-avoidant manager, shields team from executive pressure by over-promising timelines and concealing slip dates.
  3. **Priya Nair**: Deeply conscientious technologist, overwhelmed by single-handed Atlas architecture load, frustrated by lack of recognition and unkept hiring promises.
  4. **Sneha Kulkarni**: Exhausted SRE, repeatedly paged during night shifts (INC-201 at 05:12, INC-203 at 18:55, INC-205 at 20:41), relieved by contractor support but stressed by system instability.
  5. **Rahul Verma**: Diligent junior engineer, highly ethical (proactively flagged payroll overpayment), eager to learn but currently limited to API wrapper code.
  6. **Arjun Das**: Focused UI engineer, thriving in remote Pune setup, highly protective of work-life balance and anxious about return-to-office demands.
  7. **Meera Iyer**: Fiscally conservative, skeptical of marketing vanity metrics, prioritizes runway preservation above engineering expansion.
  8. **Karthik Subramanian**: Overstretched analyst balancing CFA study with finance duties; prone to procedural oversights when covering payroll.
  9. **Fatima Sheikh**: Methodical bookkeeper, takes pride in clean ledgers, frustrated when uncoordinated payroll changes occur during her planned leaves.
  10. **Deepa Joshi**: Empathetic HR leader, fiercely protective of employee psychological safety and anonymity, cautious about executive overreach.
  11. **Rohan Banerjee**: Pragmatic talent recruiter, frustrated by hiring freezes on pipeline roles he worked hard to source.
  12. **Lakshmi Pillai**: Quiet operational backbone, handles facilities, onboarding logistics, and offboarding paper trails.
  13. **Nikhil Bose**: Enthusiastic marketing leader, narrative-driven, defensive about ROI and summit spend.
  14. **Aisha Khan**: Data-oriented growth marketer, focused on CAC and paid search conversions, detached from product delivery delays.
- **Source Line / Record**: Transcripts T1-T5, Emails 01-11, Leave Register, Pulse Survey results, Git commit timestamps (Priya committing late nights at 23:47).
- **Confidence**: **Medium (M)**
- **What Would Change Your Mind**: Explicit contradictory biographical notes from company leadership.
- **Revision History**:
  - *2026-11-16*: Synthesized from data room records and behavioral indicators.

