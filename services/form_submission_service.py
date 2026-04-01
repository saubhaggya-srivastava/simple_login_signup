from sqlalchemy.orm import Session

from db.form_submission_repository import count_submissions_in_window, get_form_config
from utils.form_window import get_current_window


def _get_submission_limit_state(db: Session, user_id: int, form_id: int) -> tuple[int, int]:
    config = get_form_config(db, form_id)
    if config is None:
        raise ValueError(f"Form config not found for form_id={form_id}")

    window_start, window_end = get_current_window(config.limit_type)
    count = count_submissions_in_window(db, user_id, form_id, window_start, window_end)
    return config.limit_count, count


def can_submit(db: Session, user_id: int, form_id: int) -> bool:
    limit_count, count = _get_submission_limit_state(db, user_id, form_id)
    return count < limit_count


def get_remaining_submissions(db: Session, user_id: int, form_id: int) -> int:
    limit_count, count = _get_submission_limit_state(db, user_id, form_id)
    return max(0, limit_count - count)
