from datetime import datetime

from pydantic import BaseModel, Field


class MSLListResponse(BaseModel):
    id: int = Field(description="Primary key of the MSL record.", example=1)
    sku_parent_code: str | None = Field(default=None, description="Parent SKU code.", example="1104000700")
    sku_code: str = Field(description="SKU code.", example="1104000700")
    sku_description: str | None = Field(default=None, description="SKU description.", example="Delphy Light 40X180G")
    warehouse: int | None = Field(default=None, description="Warehouse flag.", example=1)
    hyper_a: int | None = Field(default=None, description="Hyper A flag.", example=1)
    hyper_b: int | None = Field(default=None, description="Hyper B flag.", example=1)
    super_a: int | None = Field(default=None, description="Super A flag.", example=1)
    super_b: int | None = Field(default=None, description="Super B flag.", example=1)
    minimart_a: int | None = Field(default=None, description="Minimart A flag.", example=0)
    minimart_b: int | None = Field(default=None, description="Minimart B flag.", example=0)
    grocery_a: int | None = Field(default=None, description="Grocery A flag.", example=0)
    grocery_b: int | None = Field(default=None, description="Grocery B flag.", example=0)
    grocery_c: int | None = Field(default=None, description="Grocery C flag.", example=0)
    ecom_a: int | None = Field(default=None, description="ECom A flag.", example=0)
    ecom_b: int | None = Field(default=None, description="ECom B flag.", example=0)
    petrol_pumps_a: int | None = Field(default=None, description="Petrol Pumps A flag.", example=0)
    petrol_pumps_b: int | None = Field(default=None, description="Petrol Pumps B flag.", example=0)
    petrol_pumps_c: int | None = Field(default=None, description="Petrol Pumps C flag.", example=0)
    pharmacy_a: int | None = Field(default=None, description="Pharmacy A flag.", example=0)
    pharmacy_b: int | None = Field(default=None, description="Pharmacy B flag.", example=0)
    pharmacy_c: int | None = Field(default=None, description="Pharmacy C flag.", example=0)
    wholesale: int | None = Field(default=None, description="Wholesale flag.", example=0)
    horeca: int | None = Field(default=None, description="Horeca flag.", example=0)
    created_at: datetime = Field(description="Record creation timestamp.")
    deactivated_at: datetime | None = Field(default=None, description="Deactivation timestamp if the MSL record is inactive.")


class MSLListPageResponse(BaseModel):
    items: list[MSLListResponse] = Field(description="Paginated list of MSL records.")
    total: int = Field(description="Total number of matching MSL records.", example=380)
    page: int = Field(description="Current page number.", example=1)
    limit: int = Field(description="Number of records returned per page.", example=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "sku_parent_code": "1104000700",
                        "sku_code": "1104000700",
                        "sku_description": "Delphy Light 40X180G",
                        "warehouse": 1,
                        "hyper_a": 1,
                        "hyper_b": 1,
                        "super_a": 1,
                        "super_b": 1,
                        "minimart_a": 0,
                        "minimart_b": 0,
                        "grocery_a": 0,
                        "grocery_b": 0,
                        "grocery_c": 0,
                        "ecom_a": 0,
                        "ecom_b": 0,
                        "petrol_pumps_a": 0,
                        "petrol_pumps_b": 0,
                        "petrol_pumps_c": 0,
                        "pharmacy_a": 0,
                        "pharmacy_b": 0,
                        "pharmacy_c": 0,
                        "wholesale": 0,
                        "horeca": 0,
                        "created_at": "2026-03-27T12:00:00Z",
                        "deactivated_at": None,
                    }
                ],
                "total": 380,
                "page": 1,
                "limit": 20,
            }
        }
    }


class MSLListFilterOptionsResponse(BaseModel):
    sku_parent_code: list[str]
    sku_code: list[str]
    sku_description: list[str]
    warehouse: list[int]
    hyper_a: list[int]
    hyper_b: list[int]
    super_a: list[int]
    super_b: list[int]
    minimart_a: list[int]
    minimart_b: list[int]
    grocery_a: list[int]
    grocery_b: list[int]
    grocery_c: list[int]
    ecom_a: list[int]
    ecom_b: list[int]
    petrol_pumps_a: list[int]
    petrol_pumps_b: list[int]
    petrol_pumps_c: list[int]
    pharmacy_a: list[int]
    pharmacy_b: list[int]
    pharmacy_c: list[int]
    wholesale: list[int]
    horeca: list[int]

    model_config = {
        "json_schema_extra": {
            "example": {
                "sku_parent_code": ["1104000700"],
                "sku_code": ["1104000700"],
                "sku_description": ["Delphy Light 40X180G"],
                "warehouse": [0, 1],
                "hyper_a": [0, 1],
                "hyper_b": [0, 1],
                "super_a": [0, 1],
                "super_b": [0, 1],
                "minimart_a": [0, 1],
                "minimart_b": [0, 1],
                "grocery_a": [0, 1],
                "grocery_b": [0, 1],
                "grocery_c": [0, 1],
                "ecom_a": [0, 1],
                "ecom_b": [0, 1],
                "petrol_pumps_a": [0, 1],
                "petrol_pumps_b": [0, 1],
                "petrol_pumps_c": [0, 1],
                "pharmacy_a": [0, 1],
                "pharmacy_b": [0, 1],
                "pharmacy_c": [0, 1],
                "wholesale": [0, 1],
                "horeca": [0, 1],
            }
        }
    }
