import os
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import models  # noqa: F401
from db.database import Base
from db.form_submission_repository import create_submission
from models.form_submission import FormConfig
from services.form_submission_service import can_submit, get_remaining_submissions


class FixedDateTime(datetime):
    fixed_now = datetime(2026, 3, 1, tzinfo=timezone.utc)

    @classmethod
    def now(cls, tz=None):
        if tz is None:
            return cls.fixed_now.replace(tzinfo=None)
        return cls.fixed_now.astimezone(tz)


class FormSubmissionLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.session_local()

    def tearDown(self) -> None:
        self.db.close()
        self.engine.dispose()

    def _add_form_config(self, form_id: int, limit_count: int, limit_type: str) -> None:
        self.db.add(
            FormConfig(
                form_id=form_id,
                limit_count=limit_count,
                limit_type=limit_type,
            )
        )
        self.db.commit()

    def _patch_current_time(self, fixed_now: datetime):
        FixedDateTime.fixed_now = fixed_now
        return patch("utils.form_window.datetime", FixedDateTime), patch(
            "db.form_submission_repository.datetime",
            FixedDateTime,
        )

    def test_weekly_limit_blocks_third_submission_in_same_window(self) -> None:
        self._add_form_config(form_id=101, limit_count=2, limit_type="weekly")
        user_id = 1
        fixed_now = datetime(2026, 3, 3, 10, 0, tzinfo=timezone.utc)

        patch_window, patch_repo = self._patch_current_time(fixed_now)
        with patch_window, patch_repo:
            self.assertTrue(can_submit(self.db, user_id, 101))
            create_submission(self.db, user_id, 101)

            self.assertTrue(can_submit(self.db, user_id, 101))
            create_submission(self.db, user_id, 101)

            self.assertFalse(can_submit(self.db, user_id, 101))
            self.assertEqual(get_remaining_submissions(self.db, user_id, 101), 0)

    def test_weekly_limit_resets_on_next_seven_day_bucket(self) -> None:
        self._add_form_config(form_id=102, limit_count=2, limit_type="weekly")
        user_id = 1

        patch_window, patch_repo = self._patch_current_time(
            datetime(2026, 3, 3, 10, 0, tzinfo=timezone.utc)
        )
        with patch_window, patch_repo:
            create_submission(self.db, user_id, 102)
            create_submission(self.db, user_id, 102)
            self.assertFalse(can_submit(self.db, user_id, 102))

        patch_window, patch_repo = self._patch_current_time(
            datetime(2026, 3, 8, 10, 0, tzinfo=timezone.utc)
        )
        with patch_window, patch_repo:
            self.assertTrue(can_submit(self.db, user_id, 102))
            self.assertEqual(get_remaining_submissions(self.db, user_id, 102), 2)

    def test_monthly_limit_resets_on_next_month(self) -> None:
        self._add_form_config(form_id=103, limit_count=2, limit_type="monthly")
        user_id = 1

        patch_window, patch_repo = self._patch_current_time(
            datetime(2026, 3, 20, 10, 0, tzinfo=timezone.utc)
        )
        with patch_window, patch_repo:
            create_submission(self.db, user_id, 103)
            create_submission(self.db, user_id, 103)
            self.assertFalse(can_submit(self.db, user_id, 103))
            self.assertEqual(get_remaining_submissions(self.db, user_id, 103), 0)

        patch_window, patch_repo = self._patch_current_time(
            datetime(2026, 4, 1, 0, 0, tzinfo=timezone.utc)
        )
        with patch_window, patch_repo:
            self.assertTrue(can_submit(self.db, user_id, 103))
            self.assertEqual(get_remaining_submissions(self.db, user_id, 103), 2)


if __name__ == "__main__":
    unittest.main()
