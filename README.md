# Simple Login & Signup API

A minimal FastAPI-based user authentication module using PostgreSQL and SQLAlchemy ORM.

## Project Structure

```
simple_login_signup/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── controllers/
│   ├── __init__.py
│   └── auth_controller.py  # Authentication business logic
├── db/
│   ├── __init__.py
│   └── database.py         # Engine, session factory, Base
├── models/
│   ├── __init__.py
│   └── user.py             # SQLAlchemy User model
├── schemas/
│   ├── __init__.py
│   └── user.py             # Pydantic request/response schemas
├── routes/
│   ├── __init__.py
│   └── auth.py             # Authentication endpoints
└── utils/
    ├── __init__.py
    └── security.py         # Password hashing and JWT helpers
```

## Setup

### 1. Prerequisites

- Python 3.10+
- PostgreSQL running locally (or remote)

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Edit `.env` and set your PostgreSQL connection string:

```
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/simple_login_db
JWT_SECRET_KEY=put_a_long_random_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Make sure the database `simple_login_db` exists:

```sql
CREATE DATABASE simple_login_db;
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**

### 6. Interactive docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint            | Description          |
|--------|---------------------|----------------------|
| POST   | `/signup`           | Register a new user                              |
| POST   | `/login`            | Login and set JWT auth cookie                    |
| POST   | `/logout`           | Clear JWT auth cookie                            |
| GET    | `/me`               | Get the current authenticated user from cookie   |
| PUT    | `/forgot-password`  | Update password                                  |
| GET    | `/`                 | Health check                                     |

## Authentication Notes

- Passwords are hashed using Argon2 via `pwdlib`.
- Successful login stores a JWT access token in an HttpOnly cookie named `access_token`.
- Set the cookie `secure` flag to `True` when deploying the app behind HTTPS in production.
