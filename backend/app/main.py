import logging

from fastapi import FastAPI

from app.api import auth, ping, users
from app.db import init_db

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(users.router, prefix="/users", tags=["users"])
    application.include_router(auth.router, prefix="/auth", tags=["auth"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
