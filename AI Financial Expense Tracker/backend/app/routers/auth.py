from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from app.database import get_database
from app.models import UserRole
from app.schemas import Token, UserCreate, UserPublic
from app.security import create_access_token, get_current_user, hash_password, verify_password
from app.serializers import serialize_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    now = datetime.now(timezone.utc)
    user = {
        "name": payload.name.strip(),
        "email": payload.email,
        "passwordHash": hash_password(payload.password),
        "role": UserRole.user.value,
        "createdAt": now,
        "updatedAt": now,
    }

    try:
        result = await db.users.insert_one(user)
    except DuplicateKeyError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from exc

    created_user = await db.users.find_one({"_id": result.inserted_id})
    return serialize_user(created_user)

@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await db.users.find_one(
        {"email": form_data.username.lower()}
    )

    if not user or not verify_password(
        form_data.password,
        user["passwordHash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        subject=str(user["_id"]),
        claims={"role": user.get("role", UserRole.user.value)}
    )

    return Token(access_token=token)

@router.get("/me", response_model=UserPublic)
async def read_current_user(current_user=Depends(get_current_user)):
    return serialize_user(current_user)
