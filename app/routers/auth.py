from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import RegisterRequest,LoginRequest
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password,verify_password
from app.utils.jwt_handler import create_access_token
router = APIRouter(prefix="/auth", tags=["Authentication"])

user_repo = UserRepository()


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    hashed_password = hash_password(request.password)

    user = user_repo.create_user(
        db=db,
        name=request.name,
        email=request.email,
        password=hashed_password
    )

    return {
        "status": True,
        "message": "User registered successfully",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }
    


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = user_repo.get_user_by_email(
        db=db,
        email=request.email
    )

    if not user:
        return {
            "status": False,
            "message": "Invalid email or password"
        }

    if not verify_password(request.password, user.password):
        return {
            "status": False,
            "message": "Invalid email or password"
        }
    token = create_access_token(
    data={
        "user_id": user.id,
        "email": user.email
    }
    )

    return {
    "status": True,
    "message": "Login successful",
    "access_token": token,
    "token_type": "bearer",
    "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
}