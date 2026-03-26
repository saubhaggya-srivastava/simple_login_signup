from datetime import datetime

from pydantic import BaseModel, Field


class SKUResponse(BaseModel):
    id: int = Field(description="Primary key of the SKU record.", example=1)
    sku_parent_code: str | None = Field(default=None, description="Parent SKU code.", example="PARENT001")
    sku_code: str = Field(description="Unique SKU code.", example="SKU001")
    case_barcode: str | None = Field(default=None, description="Case barcode.", example="1234567890123")
    outer_barcode: str | None = Field(default=None, description="Outer barcode.", example="2234567890123")
    unit_barcode: str | None = Field(default=None, description="Unit barcode.", example="3234567890123")
    sku_description: str | None = Field(default=None, description="SKU description.", example="Nestle milk powder 400g")
    unit_images: str | None
    outer_images: str | None
    cases_images: str | None
    master_distributor: str | None
    distributor: str | None
    line_of_business: str | None
    supplier: str | None
    agency: str | None
    category: str | None
    segment: str | None
    brand: str | None
    sub_brand: str | None
    sku_type: str | None
    promotion: str | None
    sku_status: str | None
    shelf_life_days: int | None
    temperature: str | None
    case_length_cm: float | None
    case_width_cm: float | None
    case_height_cm: float | None
    case_cbm: float | None
    outer_length_cm: float | None
    outer_width_cm: float | None
    outer_height_cm: float | None
    outer_cbm: float | None
    unit_length_cm: float | None
    unit_width_cm: float | None
    unit_height_cm: float | None
    unit_cbm: float | None
    unit_weight_gm: float | None
    outer_per_case: int | None
    units_per_outer: int | None
    case_weight_kg: float | None
    case_cost: float | None
    case_price: float | None
    outer_price: float | None
    unit_price: float | None
    unit_rsp: float | None
    created_at: datetime = Field(description="Record creation timestamp.")
    deactivated_at: datetime | None = Field(default=None, description="Deactivation timestamp if SKU is inactive.")


class SKUListResponse(BaseModel):
    items: list[SKUResponse] = Field(description="Paginated list of SKU records.")
    total: int = Field(description="Total number of matching SKU records.", example=120)
    page: int = Field(description="Current page number.", example=1)
    limit: int = Field(description="Number of records returned per page.", example=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "sku_parent_code": "PARENT001",
                        "sku_code": "SKU001",
                        "case_barcode": "1234567890123",
                        "outer_barcode": "2234567890123",
                        "unit_barcode": "3234567890123",
                        "sku_description": "Nestle milk powder 400g",
                        "unit_images": None,
                        "outer_images": None,
                        "cases_images": None,
                        "master_distributor": "ABC Group",
                        "distributor": "ABC Distribution",
                        "line_of_business": "Beverages",
                        "supplier": "Nestle",
                        "agency": "Main Agency",
                        "category": "Dairy",
                        "segment": "Premium",
                        "brand": "Nescafe",
                        "sub_brand": "Gold",
                        "sku_type": "Unit",
                        "promotion": "Yes",
                        "sku_status": "Active",
                        "shelf_life_days": 365,
                        "temperature": "Ambient",
                        "case_length_cm": 10.5,
                        "case_width_cm": 12.0,
                        "case_height_cm": 15.0,
                        "case_cbm": 0.02,
                        "outer_length_cm": 20.0,
                        "outer_width_cm": 24.0,
                        "outer_height_cm": 30.0,
                        "outer_cbm": 0.05,
                        "unit_length_cm": 5.0,
                        "unit_width_cm": 6.0,
                        "unit_height_cm": 7.0,
                        "unit_cbm": 0.001,
                        "unit_weight_gm": 400.0,
                        "outer_per_case": 2,
                        "units_per_outer": 12,
                        "case_weight_kg": 8.0,
                        "case_cost": 100.0,
                        "case_price": 120.0,
                        "outer_price": 70.0,
                        "unit_price": 10.0,
                        "unit_rsp": 12.0,
                        "created_at": "2026-03-26T12:00:00Z",
                        "deactivated_at": None,
                    }
                ],
                "total": 120,
                "page": 1,
                "limit": 20,
            }
        }
    }


class SKUFilterOptionsResponse(BaseModel):
    master_distributor: list[str]
    distributor: list[str]
    line_of_business: list[str]
    supplier: list[str]
    agency: list[str]
    category: list[str]
    segment: list[str]
    brand: list[str]
    sub_brand: list[str]
    sku_type: list[str]
    promotion: list[str]
    sku_status: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "master_distributor": ["ABC Group"],
                "distributor": ["ABC Distribution"],
                "line_of_business": ["Beverages"],
                "supplier": ["Nestle"],
                "agency": ["Main Agency"],
                "category": ["Dairy"],
                "segment": ["Premium"],
                "brand": ["Nescafe"],
                "sub_brand": ["Gold"],
                "sku_type": ["Unit"],
                "promotion": ["Yes"],
                "sku_status": ["Active"],
            }
        }
    }
