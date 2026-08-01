from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from app.database.session import Base, engine
from app.database.models.appointment import Appointment




# This creates your FastAPI application.
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the AI Receptionist project."
)

# Create database tables before initializing the FastAPI application.
Base.metadata.create_all(bind=engine)

#This defines a GET endpoint for the root URL.
@app.get("/")
def root():
    return {
         "message": f"Welcome to the {settings.APP_NAME}!"
    }

# Endpoint used to verify that the application is running.
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }

app.include_router(router)