from sqlalchemy.orm import Session

from db.form_submission_repository import count_submissions_in_window, get_form_config
from utils.form_window import get_current_window


def _get_submission_limit_state(
    db: Session,
    channel_id: int,
    form_id: int,
) -> tuple[int, int]:
    config = get_form_config(db, channel_id, form_id)
    if config is None:
        raise ValueError(
            f"Form config not found for channel_id={channel_id}, form_id={form_id}"
        )

    window_start, window_end = get_current_window(config.limit_type)
    count = count_submissions_in_window(db, channel_id, form_id, window_start, window_end)
    return config.limit_count, count


def _get_limit_label(limit_type: str) -> str:
    labels = {
        "daily": "day",
        "weekly": "week",
        "monthly": "month",
    }
    return labels.get(limit_type.lower(), limit_type.lower())


def get_submission_status(
    db: Session,
    channel_id: int,
    form_id: int,
) -> dict[str, bool | int | str]:
    config = get_form_config(db, channel_id, form_id)
    if config is None:
        raise ValueError(
            f"Form config not found for channel_id={channel_id}, form_id={form_id}"
        )

    window_start, window_end = get_current_window(config.limit_type)
    count = count_submissions_in_window(db, channel_id, form_id, window_start, window_end)
    limit_count = config.limit_count
    remaining = max(0, limit_count - count)
    allowed = remaining > 0
    limit_label = _get_limit_label(config.limit_type)

    if allowed:
        time_unit = f"this {limit_label}"
        submit_word = "time" if remaining == 1 else "times"
        message = f"You can submit {remaining} more {submit_word} {time_unit}"
    else:
        message = f"Submission limit reached for this {limit_label}"

    return {
        "allowed": allowed,
        "remaining": remaining,
        "limit": limit_count,
        "message": message,
    }


def can_submit(db: Session, channel_id: int, form_id: int) -> bool:
    limit_count, count = _get_submission_limit_state(db, channel_id, form_id)
    return count < limit_count


def get_remaining_submissions(
    db: Session,
    channel_id: int,
    form_id: int,
) -> int:
    limit_count, count = _get_submission_limit_state(db, channel_id, form_id)
    return max(0, limit_count - count)
