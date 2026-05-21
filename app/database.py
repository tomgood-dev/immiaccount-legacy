import sqlite3
import os

DATABASE = os.environ.get('DATABASE', '/data/immiaccount.db')

_db_initialized = False


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    global _db_initialized
    if _db_initialized:
        return

    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL,
            family_name TEXT NOT NULL,
            given_names TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            agent_email TEXT
        );

        CREATE TABLE IF NOT EXISTS visa_subclasses (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            stream TEXT NOT NULL,
            pathway_type TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY,
            applicant_id INTEGER NOT NULL,
            subclass_code TEXT NOT NULL,
            reference_number TEXT NOT NULL,
            date_lodged TEXT NOT NULL,
            last_updated TEXT NOT NULL,
            current_status TEXT NOT NULL,
            sponsor_name TEXT,
            FOREIGN KEY (applicant_id) REFERENCES users(id),
            FOREIGN KEY (subclass_code) REFERENCES visa_subclasses(code)
        );

        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            document_type TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT,
            amount_aud REAL NOT NULL,
            method TEXT,
            gateway_ref TEXT,
            paid_at TEXT,
            status TEXT NOT NULL,
            type TEXT,
            issuing_office TEXT,
            currency TEXT DEFAULT 'AUD',
            FOREIGN KEY (application_id) REFERENCES applications(id)
        );

        CREATE TABLE IF NOT EXISTS correspondence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT NOT NULL,
            title TEXT NOT NULL,
            date_sent TEXT NOT NULL,
            recipient_email TEXT NOT NULL,
            body TEXT,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        );

        CREATE TABLE IF NOT EXISTS status_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT NOT NULL,
            status_code TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            source_system TEXT,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        );
    """)

    conn.commit()
    conn.close()
    _db_initialized = True
