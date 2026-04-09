from pydantic import BaseModel, Field


class FormMasterBase(BaseModel):
    name: str = Field(description="Form name.", example="Warehouse", min_length=1, max_length=255)


class FormMasterCreate(FormMasterBase):
    pass


class FormMasterResponse(FormMasterBase):
    id: int = Field(description="Primary key of the form record.", example=1)


class FormMasterListResponse(BaseModel):
    items: list[FormMasterResponse] = Field(description="List of form master records.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {"id": 1, "name": "Warehouse"},
                    {"id": 2, "name": "Hyper A"},
                ]
            }
        }
    }
