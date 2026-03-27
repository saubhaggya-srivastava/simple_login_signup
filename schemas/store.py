from datetime import datetime

from pydantic import BaseModel, Field


class StoreResponse(BaseModel):
    id: int = Field(description="Primary key of the store record.", example=1)
    region: str | None = Field(default=None, description="Region.", example="Middle East")
    country: str | None = Field(default=None, description="Country.", example="Qatar")
    master_distributor: str | None = Field(default=None, description="Master distributor.", example="Abu Ali")
    retailer_code: str | None = Field(default=None, description="Retailer code.", example="131829")
    retailer_name: str | None = Field(default=None, description="Retailer name.", example="2022 HYPERMARKET")
    store_code: str = Field(description="Store code.", example="1790021")
    store_name: str | None = Field(default=None, description="Store name.", example="2022 HYPERMARKET-BIN MAHMOOD")
    store_code_distributor: str | None = Field(default=None, description="Store code (Distributor).", example="17900212")
    distributor: str | None = Field(default=None, description="Distributor.", example="Ali Products")
    store_code_lob: str | None = Field(default=None, description="Store code (LOB).", example="17900211")
    line_of_business: str | None = Field(default=None, description="Line of business.", example="Delmond")
    city: str | None = Field(default=None, description="City.", example="DOHA")
    area: str | None = Field(default=None, description="Area.", example="DOHA")
    retailer_group: str | None = Field(default=None, description="Retailer group.", example="Others")
    retailer_sub_group: str | None = Field(default=None, description="Retailer sub group.", example="Others")
    channel: str | None = Field(default=None, description="Channel.", example="Minimart")
    sub_channel: str | None = Field(default=None, description="Sub channel.", example="Minimart A")
    store_status: str | None = Field(default=None, description="Store status.", example="Active")
    central_buying: str | None = Field(default=None, description="Central buying.", example="Yes")
    central_store_code: str | None = Field(default=None, description="Central store code.", example="CSC001")
    salesmen: str | None = Field(default=None, description="Salesmen.", example="Arun Kareem")
    gps_coordinate: str | None = Field(default=None, description="GPS coordinate.", example="25.286,51.534")
    created_at: datetime = Field(description="Record creation timestamp.")
    deactivated_at: datetime | None = Field(default=None, description="Deactivation timestamp if store is inactive.")


class StoreListResponse(BaseModel):
    items: list[StoreResponse] = Field(description="Paginated list of store records.")
    total: int = Field(description="Total number of matching store records.", example=120)
    page: int = Field(description="Current page number.", example=1)
    limit: int = Field(description="Number of records returned per page.", example=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "region": "Middle East",
                        "country": "Qatar",
                        "master_distributor": "Abu Ali",
                        "retailer_code": "131829",
                        "retailer_name": "2022 HYPERMARKET",
                        "store_code": "1790021",
                        "store_name": "2022 HYPERMARKET-BIN MAHMOOD",
                        "store_code_distributor": "17900212",
                        "distributor": "Ali Products",
                        "store_code_lob": "17900211",
                        "line_of_business": "Delmond",
                        "city": "DOHA",
                        "area": "DOHA",
                        "retailer_group": "Others",
                        "retailer_sub_group": "Others",
                        "channel": "Minimart",
                        "sub_channel": "Minimart A",
                        "store_status": "Active",
                        "central_buying": None,
                        "central_store_code": None,
                        "salesmen": "Arun Kareem",
                        "gps_coordinate": "25.286,51.534",
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


class StoreFilterOptionsResponse(BaseModel):
    region: list[str]
    country: list[str]
    master_distributor: list[str]
    retailer_name: list[str]
    distributor: list[str]
    line_of_business: list[str]
    city: list[str]
    area: list[str]
    retailer_group: list[str]
    retailer_sub_group: list[str]
    channel: list[str]
    sub_channel: list[str]
    store_status: list[str]
    central_buying: list[str]
    salesmen: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "region": ["Middle East"],
                "country": ["Qatar"],
                "master_distributor": ["Abu Ali"],
                "retailer_name": ["2022 HYPERMARKET"],
                "distributor": ["Ali Products"],
                "line_of_business": ["Delmond"],
                "city": ["DOHA"],
                "area": ["DOHA"],
                "retailer_group": ["Others"],
                "retailer_sub_group": ["Others"],
                "channel": ["Minimart"],
                "sub_channel": ["Minimart A"],
                "store_status": ["Active"],
                "central_buying": ["Yes"],
                "salesmen": ["Arun Kareem"],
            }
        }
    }
