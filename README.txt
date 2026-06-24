Daily Gaming — Alpha 0.1

Turn your daily goals into a game. Track habits, complete quests, and build streaks — all through a REST API.


What is this?

Daily Gaming is a backend API for a gamified productivity app. The idea is simple: instead of boring to-do lists, your daily goals feel like quests in an RPG. Complete them, build streaks, level up.

This is an early alpha release. Only the authentication layer is implemented so far.
Frontend is not started yet — this version is backend only.


Alpha 0.1 — What is implemented

User registration
- Endpoint: POST /auth/register
- Accepts username, email, password
- Checks that username and email are not already taken
- Hashes password with bcrypt before saving to database
- If username and password match the admin credentials, the account is automatically granted admin rights

Login
- Endpoint: POST /jwt/login
- Validates username and password against the database
- Returns a signed JWT access token (RS256, RSA key pair)
- Token expires in 15 minutes

Current user info
- Endpoint: GET /jwt/users/me
- Requires a valid Bearer token in the Authorization header
- Returns username, email, admin status, and login time

Admin — reset database
- Endpoint: DELETE /admin/reset-db
- Requires a valid token from an admin account
- Clears all records from all tables


Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0 async
- SQLite + aiosqlite
- PyJWT with RS256 (RSA key pair)
- bcrypt
- Pydantic v2
- Uvicorn


Project Structure

daily_gaming/
    main.py               App entry point, lifespan, router registration
    core_config.py        JWT settings (key paths, algorithm, token TTL)
    database.py           Async SQLAlchemy engine, session factory, Base
    jwt_utils.py          encode/decode JWT, hash/validate password
    requirements.txt
    key/
        jwt_private.pem   RSA private key (gitignored)
        jwt_public.pem    RSA public key (gitignored)
    auth/
        __init__.py
        models.py         User SQLAlchemy model
        schemas.py        Pydantic schemas (UserCreate, TokenInfo, etc.)
        auth_router.py    /jwt/login and /jwt/users/me
        register_router.py  /auth/register
        admin_router.py   /admin/reset-db