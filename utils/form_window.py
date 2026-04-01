from datetime import datetime, timedelta, timezone


def get_current_window(limit_type: str) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    if limit_type == "weekly":
        days_passed = now.day - 1
        window_number = days_passed // 7
        window_start = start_of_month + timedelta(days=window_number * 7)
        window_end = window_start + timedelta(days=7)
        return window_start, window_end

    if limit_type == "monthly":
        if now.month == 12:
            next_month_start = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month_start = datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc)
        return start_of_month, next_month_start

    raise ValueError("limit_type must be 'weekly' or 'monthly'")
