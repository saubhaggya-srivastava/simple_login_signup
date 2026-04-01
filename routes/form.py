from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db.database import get_db
from db.form_submission_data_repository import insert_form_data
from db.form_submission_repository import create_submission
from schemas.form import SubmitErrorResponse, SubmitSuccessResponse
from schemas.form_schema import BaseFormSchema
from schemas.schema_map import FORM_SCHEMA_MAP
from services.form_submission_service import can_submit, get_remaining_submissions


router = APIRouter(tags=["Forms"])


def get_mock_user_id() -> int:
    return 1


@router.get(
    "/form/{form_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Get form submission status",
    description="Returns whether the current user can still submit the form in the active limit window.",
)
def get_form_status(form_id: int, db: Session = Depends(get_db)) -> dict[str, bool | int]:
    user_id = get_mock_user_id()
    remaining = get_remaining_submissions(db, user_id, form_id)
    return {
        "allowed": remaining > 0,
        "remaining_submissions": remaining,
    }


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
    payload: BaseFormSchema,
    db: Session = Depends(get_db),
) -> SubmitSuccessResponse:
    user_id = get_mock_user_id()
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
        validated_data = schema_class(**payload.model_dump())
    except ValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": str(exc),
            },
        )

    if not can_submit(db, user_id, form_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Submission limit reached",
            },
        )

    submission = create_submission(db, user_id, form_id)
    insert_form_data(db, form_id, submission.id, validated_data)
    return {"success": True}
