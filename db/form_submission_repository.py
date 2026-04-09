from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.form_submission import ChannelFormConfig, FormSubmission


def get_form_config(
    db: Session,
    channel_id: int,
    form_id: int,
) -> ChannelFormConfig | None:
    return db.execute(
        select(ChannelFormConfig).where(
            ChannelFormConfig.channel_id == channel_id,
            ChannelFormConfig.form_id == form_id,
        )
    ).scalar_one_or_none()


def count_submissions_in_window(
    db: Session,
    channel_id: int,
    form_id: int,
    window_start: datetime,
    window_end: datetime,
) -> int:
    return db.execute(
        select(func.count(FormSubmission.id)).where(
            FormSubmission.channel_id == channel_id,
            FormSubmission.form_id == form_id,
            FormSubmission.submitted_at >= window_start,
            FormSubmission.submitted_at < window_end,
        )
    ).scalar_one()


def create_submission(
    db: Session,
    channel_id: int,
    form_id: int,
    created_by: int,
) -> FormSubmission:
    submission = FormSubmission(
        channel_id=channel_id,
        form_id=form_id,
        created_by=created_by,
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
