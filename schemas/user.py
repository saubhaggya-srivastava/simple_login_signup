from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["secret123"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "secret123",
            }
        }
    }


class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=1, examples=["secret123"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "secret123",
            }
        }
    }


class ForgotPassword(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    new_password: str = Field(..., min_length=6, max_length=128, examples=["newsecret123"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "new_password": "newsecret123",
            }
        }
    }


class MessageResponse(BaseModel):
    message: str = Field(..., examples=["Operation completed successfully"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully",
            }
        }
    }

class LoginResponse(BaseModel):
    message: str = Field(..., examples=["Login successful"])
    id: int = Field(..., examples=[1])

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Login successful",
                "id": 1,
            }
        }
    }
