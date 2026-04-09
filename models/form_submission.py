from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class ChannelFormConfig(Base):
    __tablename__ = "channel_form_configs"
    __table_args__ = (
        UniqueConstraint("channel_id", "form_id", name="uq_channel_form_configs_channel_id_form_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channel_master.id"),
        nullable=False,
    )
    form_id: Mapped[int] = mapped_column(
        ForeignKey("form_master.id"),
        nullable=False,
    )
    limit_count: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class FormSubmission(Base):
    __tablename__ = "form_submissions"
    __table_args__ = (
        Index(
            "ix_form_submissions_channel_id_form_id_submitted_at",
            "channel_id",
            "form_id",
            "submitted_at",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channel_master.id"),
        nullable=False,
    )
    form_id: Mapped[int] = mapped_column(
        ForeignKey("form_master.id"),
        nullable=False,
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
