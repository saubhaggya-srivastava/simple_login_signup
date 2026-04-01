from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class FormSubmissionDataBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("form_submissions.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class WarehouseSubmissionData(FormSubmissionDataBase):
    __tablename__ = "warehouse_submissions_data"


class HyperASubmissionData(FormSubmissionDataBase):
    __tablename__ = "hyper_a_submissions_data"


class HyperBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "hyper_b_submissions_data"


class SuperASubmissionData(FormSubmissionDataBase):
    __tablename__ = "super_a_submissions_data"


class SuperBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "super_b_submissions_data"


class MinimartASubmissionData(FormSubmissionDataBase):
    __tablename__ = "minimart_a_submissions_data"


class MinimartBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "minimart_b_submissions_data"


class GroceryASubmissionData(FormSubmissionDataBase):
    __tablename__ = "grocery_a_submissions_data"


class GroceryBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "grocery_b_submissions_data"


class GroceryCSubmissionData(FormSubmissionDataBase):
    __tablename__ = "grocery_c_submissions_data"


class EcomASubmissionData(FormSubmissionDataBase):
    __tablename__ = "ecom_a_submissions_data"


class EcomBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "ecom_b_submissions_data"


class PetrolPumpsASubmissionData(FormSubmissionDataBase):
    __tablename__ = "petrol_pumps_a_submissions_data"


class PetrolPumpsBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "petrol_pumps_b_submissions_data"


class PetrolPumpsCSubmissionData(FormSubmissionDataBase):
    __tablename__ = "petrol_pumps_c_submissions_data"


class PharmacyASubmissionData(FormSubmissionDataBase):
    __tablename__ = "pharmacy_a_submissions_data"


class PharmacyBSubmissionData(FormSubmissionDataBase):
    __tablename__ = "pharmacy_b_submissions_data"


class PharmacyCSubmissionData(FormSubmissionDataBase):
    __tablename__ = "pharmacy_c_submissions_data"


class WholesaleSubmissionData(FormSubmissionDataBase):
    __tablename__ = "wholesale_submissions_data"


class HorecaSubmissionData(FormSubmissionDataBase):
    __tablename__ = "horeca_submissions_data"


FORM_MODEL_MAP: dict[int, type[FormSubmissionDataBase]] = {
    1: WarehouseSubmissionData,
    2: HyperASubmissionData,
    3: HyperBSubmissionData,
    4: SuperASubmissionData,
    5: SuperBSubmissionData,
    6: MinimartASubmissionData,
    7: MinimartBSubmissionData,
    8: GroceryASubmissionData,
    9: GroceryBSubmissionData,
    10: GroceryCSubmissionData,
    11: EcomASubmissionData,
    12: EcomBSubmissionData,
    13: PetrolPumpsASubmissionData,
    14: PetrolPumpsBSubmissionData,
    15: PetrolPumpsCSubmissionData,
    16: PharmacyASubmissionData,
    17: PharmacyBSubmissionData,
    18: PharmacyCSubmissionData,
    19: WholesaleSubmissionData,
    20: HorecaSubmissionData,
}
