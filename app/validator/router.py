from fastapi import APIRouter, Depends
from .controller import validate_token as valid_token
from data.database import get_db
from sqlalchemy.orm import Session
from data.schemes import ValidationData, ValidationSuccess, ValidationFailure
from services.exceptions import ValidationException


router = APIRouter()

@router.post("/validate-token/", tags=["validator"], response_model=ValidationSuccess, responses={400:{'model':ValidationFailure}})
def validate_token(validation_data: ValidationData, db: Session=Depends(get_db)):
    r = valid_token(validation_data, db)

    if r['status'] == 405:
        raise ValidationException()

    return r