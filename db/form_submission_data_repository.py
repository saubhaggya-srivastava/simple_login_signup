from sqlalchemy.orm import Session

from models.form_submission_data import FORM_MODEL_MAP, FormSubmissionDataBase
from schemas.form_schema import BaseFormSchema


def insert_form_data(
    db: Session,
    form_id: int,
    submission_id: int,
    payload: BaseFormSchema,
) -> FormSubmissionDataBase:
    model = FORM_MODEL_MAP.get(form_id)
    if model is None:
        raise ValueError(f"Unsupported form_id={form_id}")

    form_data = model(
        submission_id=submission_id,
        name=payload.name,
        value=payload.value,
        remarks=payload.remarks,
    )
    db.add(form_data)
    db.commit()
    db.refresh(form_data)
    return form_data
