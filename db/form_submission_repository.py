from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.form_submission import FormConfig, FormSubmission


def get_form_config(db: Session, form_id: int) -> FormConfig | None:
    return db.execute(
        select(FormConfig).where(FormConfig.form_id == form_id)
    ).scalar_one_or_none()


def count_submissions_in_window(
    db: Session,
    user_id: int,
    form_id: int,
    window_start: datetime,
    window_end: datetime,
) -> int:
    return db.execute(
        select(func.count(FormSubmission.id)).where(
            FormSubmission.user_id == user_id,
            FormSubmission.form_id == form_id,
            FormSubmission.submitted_at >= window_start,
            FormSubmission.submitted_at < window_end,
        )
    ).scalar_one()


def create_submission(db: Session, user_id: int, form_id: int) -> FormSubmission:
    submission = FormSubmission(
        user_id=user_id,
        form_id=form_id,
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
