from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class SKU(Base):
    __tablename__ = "sku_master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    sku_parent_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sku_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    case_barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    outer_barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unit_barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sku_description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    unit_images: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    outer_images: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    cases_images: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    master_distributor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    distributor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    line_of_business: Mapped[str | None] = mapped_column(String(255), nullable=True)
    supplier: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agency: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    segment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sub_brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sku_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    promotion: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sku_status: Mapped[str | None] = mapped_column(String(100), nullable=True)

    shelf_life_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    temperature: Mapped[str | None] = mapped_column(String(100), nullable=True)

    case_length_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    case_width_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    case_height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    case_cbm: Mapped[float | None] = mapped_column(Float, nullable=True)

    outer_length_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    outer_width_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    outer_height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    outer_cbm: Mapped[float | None] = mapped_column(Float, nullable=True)

    unit_length_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_width_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_cbm: Mapped[float | None] = mapped_column(Float, nullable=True)

    unit_weight_gm: Mapped[float | None] = mapped_column(Float, nullable=True)
    outer_per_case: Mapped[int | None] = mapped_column(Integer, nullable=True)
    units_per_outer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    case_weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)

    case_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    case_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    outer_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_rsp: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )