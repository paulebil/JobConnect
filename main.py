from fastapi import FastAPI

from app.routes.user import user_router, auth_user_router
from app.database.database import init_db

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app_: FastAPI):
    # startup
    await init_db()
    yield
    # shutdown (if needed, put cleanup code here)


def create_application():
    application = FastAPI(lifespan=lifespan)
    application.include_router(user_router)
    application.include_router(auth_user_router)

    return application

app = create_application()

@app.get("/")
async def health_check():
    return {"message": "Healthy JobConnect Server..."}