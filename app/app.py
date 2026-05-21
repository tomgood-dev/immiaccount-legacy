import os
import functools
from datetime import datetime, timedelta
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    get_flashed_messages,
)
from database import init_db, get_db
from seed import seed

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "immiaccount-legacy-secret-2012")
app.permanent_session_lifetime = timedelta(minutes=20)

SESSION_TIMEOUT_MINUTES = 20
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


# ---------------------------------------------------------------------------
# Initialise DB on first request
# ---------------------------------------------------------------------------

_app_initialised = False


@app.before_request
def ensure_initialised():
    global _app_initialised
    if not _app_initialised:
        init_db()
        seed()
        _app_initialised = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        last_activity = session.get("last_activity")
        if last_activity:
            elapsed = datetime.utcnow() - datetime.fromisoformat(last_activity)
            if elapsed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                session.clear()
                flash(
                    "Your session has timed out due to inactivity. Please log in again.",
                    "timeout",
                )
                return redirect(url_for("login"))

        session["last_activity"] = datetime.utcnow().isoformat()
        return f(*args, **kwargs)

    return decorated


def format_date(date_str):
    """Format ISO date string as D Mon YYYY (day without leading zero)."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        # strftime with %-d works on Linux; use lstrip on Windows
        return dt.strftime("%d %b %Y").lstrip("0")
    except (ValueError, AttributeError):
        return str(date_str)


app.jinja_env.filters["format_date"] = format_date


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return user


# ---------------------------------------------------------------------------
# Routes — Authentication
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("applications"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    timeout_msg = None

    # Retrieve flashed timeout message (set by login_required on timeout)
    for category, message in get_flashed_messages(with_categories=True):
        if category == "timeout":
            timeout_msg = message

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        db.close()

        if user:
            session.permanent = True
            session["user_id"] = user["id"]
            session["display_name"] = user["display_name"]
            session["last_activity"] = datetime.utcnow().isoformat()
            return redirect(url_for("applications"))
        else:
            error = "An error has occurred. Please check your username and password and try again."

    return render_template("login.html", error=error, timeout_msg=timeout_msg)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Routes — Applications
# ---------------------------------------------------------------------------

@app.route("/applications")
@login_required
def applications():
    user = get_current_user()
    db = get_db()
    apps = db.execute(
        """
        SELECT a.*, v.name as subclass_name, v.stream, v.pathway_type,
               u.display_name, u.date_of_birth
        FROM applications a
        JOIN visa_subclasses v ON a.subclass_code = v.code
        JOIN users u ON a.applicant_id = u.id
        WHERE a.applicant_id = ?
        ORDER BY a.last_updated DESC
        """,
        (user["id"],),
    ).fetchall()
    db.close()
    return render_template("dashboard.html", user=user, applications=apps)


@app.route("/applications/new")
@login_required
def new_application():
    user = get_current_user()
    return render_template("new_application.html", user=user)


@app.route("/applications/<app_id>")
@login_required
def app_home(app_id):
    user = get_current_user()
    db = get_db()
    application = db.execute(
        """
        SELECT a.*, v.name as subclass_name, v.stream, v.pathway_type,
               u.display_name, u.date_of_birth, u.given_names, u.family_name
        FROM applications a
        JOIN visa_subclasses v ON a.subclass_code = v.code
        JOIN users u ON a.applicant_id = u.id
        WHERE a.id = ? AND a.applicant_id = ?
        """,
        (app_id, user["id"]),
    ).fetchone()
    db.close()

    if not application:
        return redirect(url_for("applications"))

    return render_template(
        "app_home.html",
        user=user,
        application=application,
        active_tab="home",
        app_id=app_id,
    )


@app.route("/applications/<app_id>/messages")
@login_required
def app_messages(app_id):
    user = get_current_user()
    db = get_db()
    application = db.execute(
        """
        SELECT a.*, v.name as subclass_name
        FROM applications a
        JOIN visa_subclasses v ON a.subclass_code = v.code
        WHERE a.id = ? AND a.applicant_id = ?
        """,
        (app_id, user["id"]),
    ).fetchone()

    if not application:
        db.close()
        return redirect(url_for("applications"))

    correspondence = db.execute(
        """
        SELECT * FROM correspondence
        WHERE application_id = ?
        ORDER BY date_sent ASC
        """,
        (app_id,),
    ).fetchall()
    db.close()

    return render_template(
        "app_messages.html",
        user=user,
        application=application,
        correspondence=correspondence,
        active_tab="messages",
        app_id=app_id,
    )


@app.route("/applications/<app_id>/documents", methods=["GET", "POST"])
@login_required
def app_documents(app_id):
    user = get_current_user()
    db = get_db()
    application = db.execute(
        """
        SELECT a.*, v.name as subclass_name
        FROM applications a
        JOIN visa_subclasses v ON a.subclass_code = v.code
        WHERE a.id = ? AND a.applicant_id = ?
        """,
        (app_id, user["id"]),
    ).fetchone()

    if not application:
        db.close()
        return redirect(url_for("applications"))

    upload_success = False

    if request.method == "POST":
        uploaded_file = request.files.get("document_file")
        doc_type = request.form.get("document_type", "Other")

        if uploaded_file and uploaded_file.filename:
            file_data = uploaded_file.read()
            file_size = len(file_data)

            # Legacy behavior: silently drop files > 5MB, no error shown to user
            if file_size <= MAX_UPLOAD_BYTES:
                safe_filename = (
                    uploaded_file.filename
                    .replace("/", "_")
                    .replace("\\", "_")
                )
                now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                db.execute(
                    """INSERT INTO documents
                       (application_id, filename, size_bytes, document_type, uploaded_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (app_id, safe_filename, file_size, doc_type, now_str),
                )
                db.commit()
                upload_success = True
            # Files > 5MB are silently dropped — no error message displayed (legacy bug)

    documents = db.execute(
        """
        SELECT * FROM documents
        WHERE application_id = ?
        ORDER BY uploaded_at DESC
        """,
        (app_id,),
    ).fetchall()
    db.close()

    document_types = [
        "Passport",
        "Birth Certificate",
        "Employment Contract",
        "Skills Assessment",
        "Police Clearance",
        "Health Certificate",
        "Qualifications",
        "Identity Document",
        "Sponsorship Documents",
        "Other",
    ]

    return render_template(
        "app_documents.html",
        user=user,
        application=application,
        documents=documents,
        document_types=document_types,
        upload_success=upload_success,
        active_tab="documents",
        app_id=app_id,
    )


# ---------------------------------------------------------------------------
# Routes — Payments
# ---------------------------------------------------------------------------

@app.route("/payments")
@login_required
def payments():
    user = get_current_user()
    db = get_db()
    all_payments = db.execute(
        """
        SELECT p.*, a.reference_number
        FROM payments p
        LEFT JOIN applications a ON p.application_id = a.id
        WHERE a.applicant_id = ?
        """,
        (user["id"],),
    ).fetchall()
    db.close()
    return render_template("payments.html", user=user, payments=all_payments)


# ---------------------------------------------------------------------------
# Routes — Manage Account
# ---------------------------------------------------------------------------

@app.route("/manage-account", methods=["GET", "POST"])
@login_required
def manage_account():
    user = get_current_user()
    save_success = False
    save_error = None

    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if not display_name or not email:
            save_error = "An error has occurred. Please check your input and try again."
        else:
            db = get_db()
            db.execute(
                "UPDATE users SET display_name = ?, email = ?, phone = ? WHERE id = ?",
                (display_name, email, phone, user["id"]),
            )
            db.commit()
            db.close()
            session["display_name"] = display_name
            save_success = True
            user = get_current_user()

    return render_template(
        "manage_account.html",
        user=user,
        save_success=save_success,
        save_error=save_error,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
