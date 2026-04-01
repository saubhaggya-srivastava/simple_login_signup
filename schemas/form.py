from pydantic import BaseModel


class SubmitSuccessResponse(BaseModel):
    success: bool


class SubmitErrorResponse(BaseModel):
    success: bool
    message: str


class FormSubmissionDataPayload(BaseModel):
    name: str | None = None
    value: int | None = None
    remarks: str | None = None
