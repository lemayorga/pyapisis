from typing import Callable, Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    AP_NAME: str 
    AP_VERSION: str 
    APP_TITLE: str 
    APP_DESCRIPTION: str 
    ENVIROMENT: str
    DB_USER: str  
    DB_PASSWORD: str 
    DB_HOST: str 
    DB_PORT: int
    DB_NAME: str 
    DATABASE_URL: Optional[str]
    ALGORITHM: str  
    JWT_SECRET_KEY: str  
    JWT_REFRESH_SECRET_KEY: str  
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_MINUTES: str  

    @validator("DATABASE_URL", always=True)
    def composite_name(cls, v, values, **kwargs):
        uri =  f"postgresql://{values['DB_USER']}:{values['DB_PASSWORD']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        return uri

 
def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv('.env')
    settings = Settings()
    def fn() -> Settings:
        return settings

    return fn

get_settings = _configure_initial_settings()




# https://myapollo.com.tw/en/blog/python-pydantic/