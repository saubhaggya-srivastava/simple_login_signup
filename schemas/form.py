from pydantic import BaseModel, Field

from schemas.form_schema import BaseFormSchema


class SubmitSuccessResponse(BaseModel):
    success: bool


class SubmitErrorResponse(BaseModel):
    success: bool
    message: str


class FormStatusResponse(BaseModel):
    allowed: bool
    remaining: int
    limit: int
    message: str


class FormSubmitRequest(BaseModel):
    channel_id: int = Field(description="Channel id for the form submission.", example=1)
    data: BaseFormSchema
