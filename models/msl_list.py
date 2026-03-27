from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class MSLList(Base):
    __tablename__ = "msl_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    sku_parent_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sku_code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    sku_description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    warehouse: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hyper_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hyper_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    super_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    super_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    minimart_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    minimart_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grocery_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grocery_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grocery_c: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ecom_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ecom_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    petrol_pumps_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    petrol_pumps_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    petrol_pumps_c: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pharmacy_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pharmacy_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pharmacy_c: Mapped[int | None] = mapped_column(Integer, nullable=True)
    wholesale: Mapped[int | None] = mapped_column(Integer, nullable=True)
    horeca: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
