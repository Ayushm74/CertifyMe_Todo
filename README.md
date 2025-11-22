# CertifyMe Flask Todo App

A secure Flask web application for user authentication and personal todo lists. Features registration, login (session-based), logout, secure password hashing, and a full password reset flow with manual direct reset. Each user manages only their own todo items securely. Built with Flask and SQLite (SQLAlchemy ORM).

## Features
- User registration (unique email, hashed passwords)
- User login/logout (session-based)
- Password recovery and reset (manual, no emails)
- Personal dashboard with todo creation and deletion
- Only your own todos are visible/modifiable
- Secure session handling

## Requirements
- Python 3.9+
- Flask 2.3.3
- Flask_SQLAlchemy 3.1.1
- Werkzeug 3.0.1

See `requirements.txt`.

## Install & Setup
1. Clone/unzip this repo.
2. (Recommended) Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate    # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- Register your account
- Log in using email & password
- Add or delete your todo items from the dashboard
- Forgot your password? Reset it via 'Forgot Password'
- Log out securely via the dashboard or any page

## Screenshot
![Dashboard Screenshot](https://ibb.co/Z6v6XkFf)

> Add your sample screenshot to `screenshots/dashboard.png` before submission.

## Project Structure
```
CertifyMe/
  app.py               # Main Flask app logic
  models.py            # SQLAlchemy models
  requirements.txt     # Python dependencies
  static/style.css     # CSS (optional)
  templates/           # HTML templates
  README.md            # Project instructions
  certifyme.db         # SQLite DB (auto-generated)
```
# CertifyMe_Todo
