from fastapi import APIRouter, Depends
from .controller import generate_token as gen_token
from data.database import get_db
from sqlalchemy.orm import Session
from data.schemes import UserData, GenerationSuccess, GenerationFailure, FlashcallServiceUnreachable
from services.exceptions import GenerationException


router = APIRouter()

@router.post("/generate-token/", tags=["generator"], response_model=GenerationSuccess, responses={400: {"model": GenerationFailure}, 500: {"model": FlashcallServiceUnreachable}})
def generate_token(user_data: UserData, db: Session=Depends(get_db)):
    r = gen_token(user_data, db)

    if r['status'] == 405:
        raise GenerationException()

    return r


