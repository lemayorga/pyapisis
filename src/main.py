import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from config.container import Dependencies
from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routers import router

def get_application() -> FastAPI:   
    settings = get_settings()

    # print(settings.json())
    # print(settings.DATABASE_URL)

    application = FastAPI(
        title = settings.APP_TITLE,
        version = settings.AP_VERSION,
        description =  settings.APP_DESCRIPTION
    )
    application.include_router(router)

    container = Dependencies()
    # db = container.db()
    # db.create_database()
    application.container = container
    
    application.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    return application




app = get_application() 

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")


# https://ellibrodepython.com/abstract-base-class
# https://github.com/GArmane/python-fastapi-hex-todo/tree/master