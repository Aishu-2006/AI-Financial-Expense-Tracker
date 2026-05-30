# AI Financial Expense Tracker - Database & Security

This folder contains the backend foundation for the Database & Security role:

- MongoDB Atlas connection through environment variables
- Collection models and request validation
- Unique email index for users
- bcrypt password hashing
- JWT login and protected routes
- Safe response serializers that do not expose password hashes

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with your MongoDB Atlas connection string and a strong `JWT_SECRET_KEY`.

## Run

```powershell
uvicorn app.main:app --reload
```

API docs will be available at:

```text
http://127.0.0.1:8000/docs
```

## Security Notes

- Never commit the real `.env` file.
- Create a MongoDB Atlas database user with only the permissions this app needs.
- Restrict Atlas network access where possible.
- Use a long random `JWT_SECRET_KEY` in production.
- Password hashes are stored in `users.passwordHash`; plain passwords are never stored.
