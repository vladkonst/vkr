from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    api_token: str = ''
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    api_email: str
    api_pswd: str
    allowed_hosts: list #= ['*']
    allowed_origins: list
    
    class Config:
        env_file = "./.env"

settings = Settings()