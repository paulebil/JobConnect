from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user import user_router
from app.routes.jobseeker import jobseeker_router
from app.routes.employer import employer_company_profile_router
from app.routes.application import application_router
from app.routes.job import job_router

from app.database.database import init_db
from app.models.user import User
from app.models.profile import JobSeekerProfile, EmployerCompanyProfile
from app.models.job import Job
from app.models.application import Application

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
    application.include_router(jobseeker_router)
    application.include_router(employer_company_profile_router)
    application.include_router(job_router)
    application.include_router(application_router)

    return application

app = create_application()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production, e.g., ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"message": "Healthy JobConnect Server..."}