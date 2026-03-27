from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Store(Base):
    __tablename__ = "store_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(255), nullable=True)
    master_distributor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retailer_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retailer_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    store_code: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    store_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    store_code_distributor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    distributor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    store_code_lob: Mapped[str | None] = mapped_column(String(255), nullable=True)
    line_of_business: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    area: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retailer_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retailer_sub_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    channel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sub_channel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    store_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    central_buying: Mapped[str | None] = mapped_column(String(255), nullable=True)
    central_store_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salesmen: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gps_coordinate: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
