"""
Data models and SQLite schema definition for Veloxa CXO Cockpit.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "veloxa_cockpit.db")

SCHEMA_SQL = """
-- Drop tables if needed
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS jira_issues;
DROP TABLE IF EXISTS git_commits;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS on_call_rota;
DROP TABLE IF EXISTS general_ledger;
DROP TABLE IF EXISTS payroll;
DROP TABLE IF EXISTS leave_records;
DROP TABLE IF EXISTS hiring_requisitions;
DROP TABLE IF EXISTS pulse_surveys;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS transcripts;
DROP TABLE IF EXISTS entity_resolutions;
DROP TABLE IF EXISTS evidence_index;
DROP TABLE IF EXISTS simulated_activities;

-- 1. Employees
CREATE TABLE employees (
    emp_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    work_email TEXT NOT NULL,
    department TEXT NOT NULL,
    title TEXT NOT NULL,
    manager_id TEXT,
    join_date TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    exit_date TEXT,
    release_day INTEGER NOT NULL DEFAULT 1
);

-- 2. Jira Issues
CREATE TABLE jira_issues (
    key TEXT PRIMARY KEY,
    issue_type TEXT NOT NULL,
    summary TEXT NOT NULL,
    epic_link TEXT,
    assignee_initials TEXT,
    assignee_name TEXT,
    story_points INTEGER,
    status TEXT NOT NULL,
    created_date TEXT,
    resolved_date TEXT,
    fix_version TEXT,
    release_day INTEGER NOT NULL DEFAULT 3
);

-- 3. Git Commits
CREATE TABLE git_commits (
    sha TEXT PRIMARY KEY,
    author_email TEXT NOT NULL,
    author_name TEXT,
    committed_at TEXT NOT NULL,
    repo TEXT NOT NULL,
    message TEXT NOT NULL,
    files_changed INTEGER NOT NULL,
    release_day INTEGER NOT NULL DEFAULT 3
);

-- 4. PagerDuty Incidents
CREATE TABLE incidents (
    incident_id TEXT PRIMARY KEY,
    severity TEXT NOT NULL,
    opened_at TEXT NOT NULL,
    resolved_at TEXT NOT NULL,
    service TEXT NOT NULL,
    responder TEXT NOT NULL,
    duration_minutes INTEGER,
    release_day INTEGER NOT NULL DEFAULT 3
);

-- 5. On-Call Rota
CREATE TABLE on_call_rota (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_of TEXT NOT NULL,
    primary_responder TEXT NOT NULL,
    secondary_responder TEXT NOT NULL,
    release_day INTEGER NOT NULL DEFAULT 3
);

-- 6. General Ledger (Zoho Books)
CREATE TABLE general_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_date TEXT NOT NULL,
    voucher TEXT NOT NULL,
    payee TEXT NOT NULL,
    ref TEXT,
    cost_centre TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    narration TEXT,
    entered_by TEXT,
    release_day INTEGER NOT NULL DEFAULT 1
);

-- 7. Payroll Register
CREATE TABLE payroll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT NOT NULL,
    name TEXT NOT NULL,
    month TEXT NOT NULL,
    days_in_month INTEGER NOT NULL,
    days_payable INTEGER NOT NULL,
    gross_inr REAL NOT NULL,
    deductions_inr REAL NOT NULL,
    net_inr REAL NOT NULL,
    processed_by TEXT,
    release_day INTEGER NOT NULL DEFAULT 1
);

-- 8. Leave Register
CREATE TABLE leave_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    leave_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    days_taken REAL NOT NULL,
    release_day INTEGER NOT NULL DEFAULT 2
);

-- 9. Hiring Requisitions
CREATE TABLE hiring_requisitions (
    req_id TEXT PRIMARY KEY,
    role_title TEXT NOT NULL,
    department TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_date TEXT,
    target_hire_date TEXT,
    hiring_manager TEXT,
    notes TEXT,
    release_day INTEGER NOT NULL DEFAULT 2
);

-- 10. Pulse Surveys (Culture Amp)
CREATE TABLE pulse_surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quarter TEXT NOT NULL,
    department TEXT NOT NULL,
    favorability_pct INTEGER,
    participation_pct INTEGER,
    key_themes TEXT,
    release_day INTEGER NOT NULL DEFAULT 2
);

-- 11. Documents (Board updates, letters, invoices)
CREATE TABLE documents (
    doc_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    doc_date TEXT NOT NULL,
    doc_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    content_summary TEXT NOT NULL,
    release_day INTEGER NOT NULL
);

-- 12. Emails
CREATE TABLE emails (
    email_id TEXT PRIMARY KEY,
    from_addr TEXT NOT NULL,
    to_addr TEXT NOT NULL,
    sent_date TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    release_day INTEGER NOT NULL
);

-- 13. Transcripts & Voice Notes
CREATE TABLE transcripts (
    transcript_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    speaker TEXT NOT NULL,
    call_date TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    key_takeaways TEXT NOT NULL,
    release_day INTEGER NOT NULL
);

-- 14. Entity Resolutions
CREATE TABLE entity_resolutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_identifier TEXT NOT NULL,
    seen_in_file TEXT NOT NULL,
    resolves_to TEXT NOT NULL,
    kind TEXT NOT NULL,
    evidence_refs TEXT,
    confidence TEXT NOT NULL DEFAULT 'H'
);

-- 15. Evidence Index (Official 60 facts)
CREATE TABLE evidence_index (
    ref_id TEXT PRIMARY KEY,
    file_source TEXT NOT NULL,
    location_ref TEXT NOT NULL,
    fact_statement TEXT NOT NULL,
    entities_named TEXT,
    date_as_written TEXT,
    date_normalized TEXT,
    confidence TEXT NOT NULL DEFAULT 'H',
    release_day INTEGER NOT NULL
);

-- 16. Simulated Autonomous Activities (Post Oct 31, 2026)
CREATE TABLE simulated_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    actor_name TEXT NOT NULL,
    activity_type TEXT NOT NULL, -- 'git_commit', 'handover_doc', 'on_call_shift', 'jira_update', 'status_email'
    summary TEXT NOT NULL,
    details TEXT NOT NULL
);
"""

def get_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DB_PATH):
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)

