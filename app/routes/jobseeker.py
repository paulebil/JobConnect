from fastapi import APIRouter, Form, UploadFile

jobseeker_router = APIRouter(
    tags=["JobSeeker"]
)

@jobseeker_router.post("/profile")
async def create_profile():
    pass