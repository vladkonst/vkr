from fastapi import Depends, FastAPI, Request
from data.database import get_db
from data.crud import get_secret_key
from sqlalchemy.orm import Session
from services.config import settings
from services.flashcall_service import get_auth_token
from generator.router import router as gen_router
from validator.router import router as valid_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from services.exceptions import GenerationException, ValidationException
from fastapi.responses import JSONResponse


description = """
    Сервис двухфакторной аутентификации на базе авторизации по звонку.
    Позволяет генерировать одноразовые пароли, отправлять их пользователю при помощи flashcall а также их валидировать.
    
    generator
    Позволяет генерировать одноразовые пароли а также отправляет их после генерации на указанный номер телефона.

    validator
    Позволяет валидировать одноразовые пароли.
"""

tags_metadata = [
    {
        "name": "generator",
        "description": "Генерация одноразовых паролей.",
    },
    {
        "name": "validator",
        "description": "Валидация одноразовых паролей.",
    },
]

app = FastAPI(title='2FA service', description=description, openapi_tags=tags_metadata)

@app.exception_handler(GenerationException)
async def generation_exception_handler(request: Request, exc: GenerationException):
    return JSONResponse(
        status_code=400,
        content={"message": "превышено допустимое количество генераций."},
    )

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={"message": "not validated."},
    )

origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts
)

@app.on_event('startup')
def init_settings():
    settings.api_token = get_auth_token()


app.include_router(gen_router)
app.include_router(valid_router)

@app.get("/")
def root(session: Session = Depends(get_db)):
    return {"message": get_secret_key(session)}