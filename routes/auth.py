from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from schemas.user import UserSignup, UserLogin, ForgotPassword, MessageResponse, LoginResponse

router = APIRouter(tags=["Authentication"])


@router.post(
    "/signup",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(payload: UserSignup, db: Session = Depends(get_db)) -> MessageResponse:
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(email=payload.email, password=payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return MessageResponse(message="User registered successfully")


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> MessageResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or user.password != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return LoginResponse(message="Login successful", id=user.id)


@router.put(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def forgot_password(payload: ForgotPassword, db: Session = Depends(get_db)) -> MessageResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.password = payload.new_password
    db.commit()

    return MessageResponse(message="Password updated successfully")
