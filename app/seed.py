import sys
import os

# Allow running directly or via import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db


def seed():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # --- Users ---
    existing_user = cursor.execute(
        "SELECT id FROM users WHERE username = ?", ("swilson",)
    ).fetchone()

    if not existing_user:
        cursor.execute(
            """INSERT INTO users
               (username, password, display_name, family_name, given_names,
                date_of_birth, email, phone, agent_email)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "swilson",
                "Password1",
                "WILSON, Samuel Chimwemwe",
                "WILSON",
                "Samuel Chimwemwe",
                "1995-07-03",
                "samuel.wilson@email.com",
                "+61 412 345 678",
                "ANTHONY@VISACORP.COM.AU",
            ),
        )

    # --- Visa subclasses ---
    subclasses = [
        ("482", "482 - Temporary Skill Shortage", "Skilled", "Temporary"),
        ("186", "Employer Nomination Scheme (186, 187)", "Skilled", "Permanent"),
        ("187", "Regional Sponsored Migration Scheme (187)", "Skilled", "Permanent"),
        ("189", "Skilled - Independent (189)", "Skilled", "Permanent"),
        ("190", "Skilled - Nominated (190)", "Skilled", "Permanent"),
        ("491", "Skilled - Work Regional (491)", "Skilled", "Temporary"),
        ("500", "Student (500)", "Student", "Temporary"),
        ("600", "Visitor (600)", "Visitor", "Temporary"),
        ("820", "Partner (820/801)", "Family", "Temporary"),
        ("801", "Partner (820/801)", "Family", "Permanent"),
        ("300", "Prospective Marriage (300)", "Family", "Temporary"),
        ("103", "Parent (103)", "Family", "Permanent"),
        ("143", "Contributory Parent (143)", "Family", "Permanent"),
        ("407", "Training (407)", "Temporary Work", "Temporary"),
        ("408", "Temporary Activity (408)", "Temporary Work", "Temporary"),
        ("417", "Working Holiday (417)", "Working Holiday Maker", "Temporary"),
        ("462", "Work and Holiday (462)", "Working Holiday Maker", "Temporary"),
        ("485", "Temporary Graduate (485)", "Skilled", "Temporary"),
        ("400", "Temporary Work (Short Stay Specialist) (400)", "Temporary Work", "Temporary"),
        ("403", "Temporary Work (International Relations) (403)", "Temporary Work", "Temporary"),
        ("200", "Refugee (200)", "Refugee & Humanitarian", "Permanent"),
        ("202", "Global Special Humanitarian (202)", "Refugee & Humanitarian", "Permanent"),
        ("761", "Resident Return (155/157)", "Resident Return", "Permanent"),
        ("132", "Business Talent (132)", "Business Innovation", "Permanent"),
        ("888", "Business Innovation and Investment (888)", "Business Innovation", "Permanent"),
    ]

    for sc in subclasses:
        existing = cursor.execute(
            "SELECT code FROM visa_subclasses WHERE code = ?", (sc[0],)
        ).fetchone()
        if not existing:
            cursor.execute(
                "INSERT INTO visa_subclasses (code, name, stream, pathway_type) VALUES (?, ?, ?, ?)",
                sc,
            )

    # --- Applications ---
    user = cursor.execute(
        "SELECT id FROM users WHERE username = ?", ("swilson",)
    ).fetchone()
    user_id = user["id"]

    existing_app1 = cursor.execute(
        "SELECT id FROM applications WHERE id = ?", ("app-001",)
    ).fetchone()
    if not existing_app1:
        cursor.execute(
            """INSERT INTO applications
               (id, applicant_id, subclass_code, reference_number,
                date_lodged, last_updated, current_status, sponsor_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "app-001",
                user_id,
                "186",
                "EGP7U7446E",
                "2025-06-06",
                "2025-06-18",
                "Received",
                "Acme Engineering Pty Ltd",
            ),
        )

    existing_app2 = cursor.execute(
        "SELECT id FROM applications WHERE id = ?", ("app-002",)
    ).fetchone()
    if not existing_app2:
        cursor.execute(
            """INSERT INTO applications
               (id, applicant_id, subclass_code, reference_number,
                date_lodged, last_updated, current_status, sponsor_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "app-002",
                user_id,
                "482",
                "TMP4K9812F",
                "2023-03-15",
                "2024-11-20",
                "Finalised",
                None,
            ),
        )

    # --- Correspondence for app-001 ---
    existing_corr = cursor.execute(
        "SELECT id FROM correspondence WHERE application_id = ?", ("app-001",)
    ).fetchone()
    if not existing_corr:
        correspondence_rows = [
            (
                "app-001",
                "IMMI Acknowledgement of Application Received",
                "2025-06-06",
                "ANTHONY@VISACORP.COM.AU",
                "Your application has been received and is being processed.",
            ),
            (
                "app-001",
                "Request for Health Examinations",
                "2025-06-06",
                "ANTHONY@VISACORP.COM.AU",
                "You are required to undertake health examinations as part of your visa application.",
            ),
            (
                "app-001",
                "IMMI Bridging Visa Grant Notification",
                "2025-06-06",
                "ANTHONY@VISACORP.COM.AU",
                "A Bridging Visa has been granted to allow you to remain lawfully in Australia.",
            ),
            (
                "app-001",
                "IMMI Bridging Visa Grant Notification",
                "2026-05-05",
                "ANTHONY@VISACORP.COM.AU",
                "A Bridging Visa has been granted to allow you to remain lawfully in Australia.",
            ),
        ]
        for row in correspondence_rows:
            cursor.execute(
                """INSERT INTO correspondence
                   (application_id, title, date_sent, recipient_email, body)
                   VALUES (?, ?, ?, ?, ?)""",
                row,
            )

    conn.commit()
    conn.close()
    print("Seed data loaded successfully.")


if __name__ == "__main__":
    seed()
