from pydantic import BaseModel, Field


class ChannelBase(BaseModel):
    name: str = Field(description="Channel name.", example="Warehouse", min_length=1, max_length=255)


class ChannelCreate(ChannelBase):
    pass


class ChannelResponse(ChannelBase):
    id: int = Field(description="Primary key of the channel record.", example=1)


class ChannelListResponse(BaseModel):
    items: list[ChannelResponse] = Field(description="List of channel records.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {"id": 1, "name": "Warehouse"},
                    {"id": 2, "name": "Hyper A"},
                    {"id": 3, "name": "Minimart B"},
                    {"id": 4, "name": "Grocery A"},
                ]
            }
        }
    }
