import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
DB_PATH = os.path.join(os.path.dirname(__file__), "portal.db")

QUIZ = [
    {
        "question": "You receive an email asking you to verify your bank account through an unfamiliar link. What should you do?",
        "options": ["Click the link immediately", "Reply with your password", "Avoid the link and verify through the bank's official channel", "Forward it to everyone"],
        "answer": 2,
        "explanation": "Unexpected links and urgent requests are common phishing signs. Verify independently using the official website or phone number."
    },
    {
        "question": "Which password is generally the strongest?",
        "options": ["password123", "Santhosine2005", "Qwerty@123", "A long, unique passphrase not reused elsewhere"],
        "answer": 3,
        "explanation": "Length and uniqueness matter. Use a password manager to create and store unique passwords."
    },
    {
        "question": "What does HTTPS primarily provide?",
        "options": ["A guarantee that a website is honest", "Encryption in transit between browser and website", "Protection from every malware attack", "Free antivirus protection"],
        "answer": 1,
        "explanation": "HTTPS encrypts data in transit, but it does not prove that the site itself is trustworthy."
    },
    {
        "question": "You find an unknown USB drive in the college lab. What is the safest action?",
        "options": ["Plug it in to identify the owner", "Use it on your personal laptop", "Give it to the responsible IT staff without plugging it in", "Copy its files"],
        "answer": 2,
        "explanation": "Unknown removable media can contain malicious files. Hand it to IT staff."
    },
    {
        "question": "What should you do if you suspect your account has been compromised?",
        "options": ["Ignore it", "Change the password from a trusted device, enable MFA, and report it", "Share the OTP with support", "Delete all emails"],
        "answer": 1,
        "explanation": "Secure the account from a trusted device, enable multi-factor authentication, and notify the appropriate support team."
    }
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incident_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                contact TEXT,
                created_at TEXT NOT NULL
            )
        """)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        answers = request.form
        score = 0
        results = []
        for i, item in enumerate(QUIZ):
            selected = answers.get(f"q{i}", "")
            correct = str(item["answer"])
            is_correct = selected == correct
            score += int(is_correct)
            results.append({
                "question": item["question"],
                "selected": item["options"][int(selected)] if selected.isdigit() and int(selected) < len(item["options"]) else "Not answered",
                "correct": item["options"][item["answer"]],
                "is_correct": is_correct,
                "explanation": item["explanation"]
            })
        return render_template("quiz_result.html", score=score, total=len(QUIZ), results=results)
    return render_template("quiz.html", questions=QUIZ)

@app.route("/password-checker")
def password_checker():
    return render_template("password.html")

@app.route("/api/password-strength", methods=["POST"])
def password_strength():
    password = request.get_json(silent=True) or {}
    value = password.get("password", "")
    # This checker evaluates locally submitted text only; it never stores the password.
    score = 0
    if len(value) >= 12: score += 2
    elif len(value) >= 8: score += 1
    if any(c.islower() for c in value): score += 1
    if any(c.isupper() for c in value): score += 1
    if any(c.isdigit() for c in value): score += 1
    if any(not c.isalnum() for c in value): score += 1
    labels = ["Very weak", "Weak", "Fair", "Good", "Strong", "Strong", "Very strong"]
    return jsonify({"score": score, "label": labels[min(score, 6)]})

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        contact = request.form.get("contact", "").strip()
        if not category or not description:
            flash("Please select a category and enter a description.", "error")
            return redirect(url_for("report"))
        if len(description) > 2000 or len(contact) > 120:
            flash("Input is too long. Please shorten it and try again.", "error")
            return redirect(url_for("report"))
        with get_db() as conn:
            conn.execute(
                "INSERT INTO incident_reports (category, description, contact, created_at) VALUES (?, ?, ?, ?)",
                (category, description, contact, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        flash("Your demo incident report has been submitted successfully.", "success")
        return redirect(url_for("report"))
    return render_template("report.html")

@app.route("/admin/reports")
def admin_reports():
    # Demo-only page. Add authentication and authorization before any real deployment.
    with get_db() as conn:
        reports = conn.execute("SELECT * FROM incident_reports ORDER BY id DESC").fetchall()
    return render_template("admin.html", reports=reports)

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
