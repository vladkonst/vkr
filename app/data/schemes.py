from pydantic import Field, BaseModel
from uuid import UUID


class UserData(BaseModel):
    UUID: UUID
    phone_number: str

class ValidationData(BaseModel):
    UUID: UUID
    otp: str

class GenerationSuccess(BaseModel):
    message: str
    status: int
    call_details: dict

class FlashcallServiceUnreachable(BaseModel):
    message: str
    status: int

class GenerationFailure(BaseModel):
    message: str
    status: int

class ValidationSuccess(BaseModel):
    message: str
    status: int

class ValidationFailure(BaseModel):
    message: str
    status: int