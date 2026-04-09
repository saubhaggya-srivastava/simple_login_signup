from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from controllers.auth_controller import get_current_user
from db.database import get_db
from db.form_submission_data_repository import insert_form_data
from db.form_submission_repository import create_submission
from models.user import User
from schemas.form import (
    FormStatusResponse,
    FormSubmitRequest,
    SubmitErrorResponse,
    SubmitSuccessResponse,
)
from schemas.schema_map import FORM_SCHEMA_MAP
from services.form_submission_service import can_submit, get_submission_status


router = APIRouter(tags=["Forms"])


@router.get(
    "/form/{form_id}/status",
    response_model=FormStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get form submission status",
    description="Returns whether the current user can still submit the form in the active limit window.",
)
def get_form_status(
    form_id: int,
    channel_id: int = Query(..., description="Channel id to resolve the form limit config."),
    db: Session = Depends(get_db),
) -> FormStatusResponse:
    try:
        status_payload = get_submission_status(db, channel_id, form_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return FormStatusResponse(**status_payload)


@router.post(
    "/form/{form_id}/submit",
    status_code=status.HTTP_200_OK,
    response_model=SubmitSuccessResponse,
    responses={
        400: {
            "model": SubmitErrorResponse,
        }
    },
    summary="Submit form",
    description="Creates a form submission only if the backend limit check allows it.",
)
def submit_form(
    form_id: int,
    payload: FormSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubmitSuccessResponse:
    channel_id = payload.channel_id
    schema_class = FORM_SCHEMA_MAP.get(form_id)

    if schema_class is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Invalid form_id",
            },
        )

    try:
        validated_data = schema_class(**payload.data.model_dump())
    except ValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": str(exc),
            },
        )

    try:
        allowed = can_submit(db, channel_id, form_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if not allowed:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Submission limit reached",
            },
        )

    submission = create_submission(db, channel_id, form_id, current_user.id)
    insert_form_data(db, form_id, submission.id, validated_data)
    return {"success": True}
