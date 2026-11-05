# Cybersecurity Awareness Portal

A Flask-based Network Security mini project for learning and demonstrating cybersecurity awareness.

## Features
- Home dashboard with navigation
- Awareness library: phishing, malware, passwords/MFA, public Wi-Fi, social engineering, and privacy
- 5-question cybersecurity quiz with score and explanations
- Basic password-strength estimator (use a sample password only)
- Incident reporting form backed by SQLite
- Local demo admin page to view submitted reports

## Requirements
- Python 3.9 or newer
- pip

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt or VS Code terminal in the project folder.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it:
   `venv\\Scripts\\activate`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Start the application:
   `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.

## Run on macOS/Linux
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python app.py`
5. Open `http://127.0.0.1:5000`

## Demo admin page
Open `http://127.0.0.1:5000/admin/reports` to view submitted demo reports.

## Project structure
```
Cybersecurity_Awareness_Portal/
├── app.py
├── requirements.txt
├── README.md
├── portal.db                 # created automatically after first run
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── learn.html
│   ├── quiz.html
│   ├── quiz_result.html
│   ├── password.html
│   ├── report.html
│   ├── admin.html
│   ├── about.html
│   └── 404.html
└── static/
    ├── style.css
    └── script.js
```

## Important academic / security notes
- The password checker is a basic educational estimate. Do not enter a real password.
- The incident report form stores demo reports in a local SQLite database.
- The admin page is intentionally unauthenticated for local classroom demonstration only.
- Before real deployment, add authentication and role-based authorization, CSRF protection, HTTPS, input/output security review, secure secret management, logging, retention rules, and privacy notice.
- This application does not detect live attacks, scan devices, or verify whether a submitted URL is malicious.
