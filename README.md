# DailyGame — Beta 1.0

Turn your daily goals into a game. Track habits, complete quests, and build streaks.

---

## What is this?

DailyGame is a gamified productivity app. Instead of boring to-do lists, your daily goals feel like quests in an RPG. Complete them, build streaks, level up.

Beta 1.0 — first fully functional release with backend, frontend, and admin panel.

---

## Beta 1.0 — What is implemented

### Auth
- `POST /auth/register` — registration with username, email, password. Admin rights granted if credentials match `.env`
- `POST /jwt/login` — returns signed JWT access token (RS256)
- `GET /jwt/users/me` — current user info

### Goals
- `POST /goals` — create a goal
- `GET /goals` — get all your goals
- `GET /goals/{id}` — get a single goal
- `PATCH /goals/{id}` — edit title, description, scheduled date
- `PATCH /goals/{id}/complete` — mark goal as completed, updates streak
- `DELETE /goals/{id}` — delete a goal

### Admin
- `GET /admin/users` — list all users
- `DELETE /admin/users/{id}` — delete a specific user
- `DELETE /admin/reset-db` — wipe all users from the database

### Frontend
- Login page
- Register page
- Main page with goal cards (streak progress bar, hover menu)
- Create goal page
- Edit goal page
- Admin panel (user list, delete user, reset DB)

---

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0 async
- SQLite + aiosqlite
- PyJWT with RS256 (RSA key pair)
- bcrypt
- Pydantic v2
- Uvicorn
- HTML + CSS + Vanilla JS

---

## Project Structure

```
daily_game/
├── main.py                 App entry point, lifespan, router registration
├── core_config.py          JWT + admin settings (reads from .env)
├── database.py             Async SQLAlchemy engine, session factory, Base
├── jwt_utils.py            encode/decode JWT, hash/validate password
├── requirements.txt
├── start.bat               Start both servers in one click
├── stop.bat                Stop both servers in one click
├── .env                    Admin credentials (not in git)
├── .env.example            Template for .env
├── key/
│   ├── jwt_private.pem     RSA private key (not in git)
│   └── jwt_public.pem      RSA public key (not in git)
├── auth/
│   ├── models.py           User SQLAlchemy model
│   ├── schemas.py          Pydantic schemas
│   ├── auth_router.py      /jwt/login and /jwt/users/me
│   ├── register_router.py  /auth/register
│   └── admin_router.py     /admin/* endpoints
├── goals/
│   ├── goal_models.py      Goal SQLAlchemy model
│   ├── goal_schemas.py     Pydantic schemas
│   ├── goal_router.py      /goals/* endpoints
│   └── goal_service.py     Business logic, streak system
└── FrontEnd/
    ├── login.html
    ├── register.html
    ├── index.html
    ├── create-goal.html
    ├── edit-goal.html
    └── admin.html
```

---

## Setup

### 1. Clone and create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
pip install python-multipart
```

### 2. Generate RSA keys
```bash
python -c "
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os; os.makedirs('key', exist_ok=True)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
with open('key/jwt_private.pem', 'wb') as f:
    f.write(private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
with open('key/jwt_public.pem', 'wb') as f:
    f.write(private_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
print('Keys created!')
"
```

### 3. Create .env file
```
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_strong_password
```

### 4. Run
Double-click `start.bat` — both servers start and browser opens automatically.

To stop — double-click `stop.bat`.

---

## Notes

- Register with admin credentials from `.env` to get admin rights
- Admin panel available at `/admin.html` (button visible in header when logged in as admin)
- `.env`, `key/` and `app.db` are gitignored — never commit them