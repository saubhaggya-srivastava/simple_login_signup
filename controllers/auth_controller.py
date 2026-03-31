from fastapi import Cookie, Depends, HTTPException, Response, status
from jose import JWTError
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from schemas.user import CurrentUserResponse, ForgotPassword, LoginResponse, MessageResponse, UserLogin, UserSignup
from utils.security import create_access_token, decode_access_token, hash_password, verify_password


COOKIE_NAME = "access_token"


def signup_user(payload: UserSignup, db: Session) -> MessageResponse:
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(payload.password)
    new_user = User(email=payload.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return MessageResponse(message="User registered successfully")


def login_user(payload: UserLogin, response: Response, db: Session) -> LoginResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"user_id": user.id})
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,  # Switch to True when the app is served over HTTPS.
        samesite="lax",
        max_age=30 * 60,
        path="/",
    )

    return LoginResponse(
        message="Login successful",
        id=user.id,
        access_token=access_token,
        token_type="bearer",
    )


def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_access_token(access_token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def get_current_user_profile(current_user: User) -> CurrentUserResponse:
    return CurrentUserResponse(id=current_user.id, email=current_user.email)


def logout_user(response: Response) -> MessageResponse:
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        samesite="lax",
    )
    return MessageResponse(message="Logged out successfully")


def reset_password(payload: ForgotPassword, db: Session) -> MessageResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.password = hash_password(payload.new_password)
    db.commit()

    return MessageResponse(message="Password updated successfully")
