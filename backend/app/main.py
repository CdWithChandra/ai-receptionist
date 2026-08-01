from fastapi import FastAPI
from app.config import settings


# This creates your FastAPI application.
app=FastAPI (
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the AI Receptionist project."
)
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
    