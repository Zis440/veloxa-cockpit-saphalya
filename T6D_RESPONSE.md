# Response to CEO Voice Note T6d

**To**: Ananya Rao, CEO  
**From**: Saphalya (`veloxa-cockpit-saphalya`)  
**Date**: Thursday, 19 November 2026 (Day 4 Deliverable)  
**Subject**: Urgent: Impact of Priya Nair's Resignation on Atlas v3 & Board Strategy (Voice Note T6d)  
**Decision**: **Crisis Impact Assessment Delivered & Board Milestone Reset Recommended**

---

### Ananya's Voice Note T6d (Received 19 Nov 2026):
> *"Bad news, Pria resigned this morning. Notice period two months, I think. What does this do to version three? I need to know before the board call."*

---

### My Crisis Assessment & Action Plan

Hi Ananya,

Priya Nair’s resignation this morning is a tier-1 existential crisis for the Atlas (routing engine v3) program. Here is the unvarnished analysis of what this does to version 3 before you speak with the board:

---

### 1. The Hard Numbers & Dependency Concentration
Across Veloxa's engineering data room, Priya Nair is our single point of failure:
- **Codebase Dominance**: Priya authored **588 of 1,453 total commits (over 40%)** across all company repositories, and over **80% of `atlas-engine`**.
- **Jira Ownership**: She is the sole assignee on **28 core tickets** across Epic ATLAS-1 (*Core routing engine v3*) and Epic ATLAS-2 (*Real-time re-routing*).
- **Knowledge Gap**: 
  - Rahul Verma (`VX018`) joined in February and has worked exclusively on `atlas-api` (237 commits).
  - Arjun Das (`VX009`) is dedicated to frontend `planner-web` from Pune (348 commits).
  - Sneha Kulkarni (`VX012`) is consumed by SRE and incident recovery.
  - **No other engineer understands the multi-stop routing graph optimization algorithms or heuristic pruning rules.**

---

### 2. What This Does to Version 3
1. **The 15 December GA is Unachievable**:
   - Atlas GA was originally promised to the board for **15 September 2026**.
   - On **2 September 2026**, Vikram quietly moved the release date in Jira to **15 December 2026** (`Jira_Export_ATLAS.xlsx`, Versions tab).
   - With Priya now on a 2-month notice period (effective through mid-January 2027), **Atlas v3 cannot launch as General Availability on 15 December**. Attempting to force a December GA without Priya will lead to catastrophic routing engine crashes for enterprise logistics clients.
2. **Underlying Cause**:
   - Priya’s late-night email on 1 September (`09.eml`: *"Can we talk about Atlas ownership sometime this week?"*) and her sparse leave record (only 2 days taken all year) show she was carrying the entire engineering output alone while backend hiring was frozen (REQ-014/015).

---

### 3. Concrete Action Plan for Your Board Call

#### Immediate Step (Today): Retention Discussion
Schedule an emergency 1:1 with Priya today before the board call. Offer:
- Title promotion to **Principal Architect & Fellow**.
- Significant equity top-up and revised market compensation.
- Direct veto power over backend hiring (unfreezing REQ-014 and REQ-015 immediately).

#### If Priya Confirms Resignation: Structured Knowledge Transfer
- **Zero New Features**: Mandate that Priya writes no new code during her notice period.
- **100% Pair Programming**: 100% of her remaining time must be spent pair-programming with Rahul Verma and an urgent senior external contractor on graph heuristics and edge-case recovery.

#### How to Position This on the Board Call:
Do **not** promise December 15 GA. Transparently explain:
> *"Following reliability hardening in August and a critical engineering leadership transition, Veloxa is shipping an Atlas Private Beta to 3 select design partners in December 2026. Production General Availability is rescheduled to **Q1 FY27 (late February / early March 2027)** once architectural knowledge transfer is completed."*
