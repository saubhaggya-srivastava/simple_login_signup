from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from controllers.auth_controller import (
    get_current_user,
    get_current_user_profile,
    login_user,
    logout_user,
    reset_password,
    signup_user,
)
from db.database import get_db
from models.user import User
from schemas.user import CurrentUserResponse, ForgotPassword, LoginResponse, MessageResponse, UserLogin, UserSignup


router = APIRouter(tags=["Authentication"])


@router.post(
    "/signup",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account if the email address is not already registered.",
    responses={
        201: {"description": "User registered successfully."},
        400: {"description": "Email already exists."},
    },
)
def signup(payload: UserSignup, db: Session = Depends(get_db)) -> MessageResponse:
    return signup_user(payload, db)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description=(
        "Validates email and password, stores the JWT access token in an HttpOnly cookie, "
        "and also returns the token in the response body for easier Swagger testing."
    ),
    responses={
        200: {"description": "Login successful."},
        401: {"description": "Invalid email or password."},
    },
)
def login(
    payload: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
) -> LoginResponse:
    return login_user(payload, response, db)


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Clears the authentication cookie from the browser.",
)
def logout(response: Response) -> MessageResponse:
    return logout_user(response)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Returns the currently authenticated user using the JWT cookie set by `/login`.",
    responses={
        200: {"description": "Authenticated user returned successfully."},
        401: {"description": "Authentication cookie is missing, invalid, or expired."},
    },
)
def get_me(current_user: User = Depends(get_current_user)) -> CurrentUserResponse:
    return get_current_user_profile(current_user)


@router.put(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset a user's password",
    description="Updates the password for an existing user identified by email.",
    responses={
        200: {"description": "Password updated successfully."},
        404: {"description": "User not found."},
    },
)
def forgot_password(payload: ForgotPassword, db: Session = Depends(get_db)) -> MessageResponse:
    return reset_password(payload, db)
