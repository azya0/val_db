from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings

from routers import __all__ as routers


def get_application(settings):
    application = FastAPI(
        title='Муталимова В.М.',
        version='dev',
        debug=True,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        application.include_router(router)

    return application


app = get_application(get_settings())
