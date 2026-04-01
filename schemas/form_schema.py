from pydantic import BaseModel


class BaseFormSchema(BaseModel):
    name: str | None = None
    value: int | None = None
    remarks: str | None = None
