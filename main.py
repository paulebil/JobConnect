from fastapi import FastAPI

def create_application():
    application = FastAPI()
    return application

app = create_application()

@app.get("/")
async def health_check():
    return {"message": "Healthy JobConnect Server..."}