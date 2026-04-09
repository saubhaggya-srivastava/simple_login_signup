from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, func
from sqlalchemy.orm import Session

from db.database import get_db
from models.form_master import FormMaster
from schemas.form_master import (
    FormMasterCreate,
    FormMasterListResponse,
    FormMasterResponse,
)

router = APIRouter(prefix="/forms-master", tags=["Form Master"])


def serialize_form_master(form: FormMaster) -> dict[str, int | str]:
    return {
        "id": form.id,
        "name": form.name,
    }


@router.get(
    "",
    response_model=FormMasterListResponse,
    status_code=status.HTTP_200_OK,
    summary="List form master records",
    description="Returns all form master records ordered by `id`.",
    responses={200: {"description": "Form master list returned successfully."}},
)
def list_form_master(db: Session = Depends(get_db)) -> FormMasterListResponse:
    items = db.query(FormMaster).order_by(asc(FormMaster.id)).all()
    return FormMasterListResponse(items=[serialize_form_master(item) for item in items])


@router.post(
    "",
    response_model=FormMasterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create form master record",
    description="Creates a new form master record. This endpoint is open for now.",
    responses={
        201: {"description": "Form master record created successfully."},
        400: {"description": "Form name is blank."},
        409: {"description": "Form name already exists."},
    },
)
def create_form_master(
    payload: FormMasterCreate,
    db: Session = Depends(get_db),
) -> FormMasterResponse:
    cleaned_name = payload.name.strip()
    if not cleaned_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Form name cannot be blank.",
        )

    existing_form = (
        db.query(FormMaster)
        .filter(func.lower(FormMaster.name) == cleaned_name.lower())
        .first()
    )
    if existing_form is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Form name already exists.",
        )

    form = FormMaster(name=cleaned_name)
    db.add(form)
    db.commit()
    db.refresh(form)

    return FormMasterResponse(**serialize_form_master(form))
