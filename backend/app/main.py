from fastapi import FastAPI

# This creates your FastAPI application.
app=FastAPI (
    title="AI Receptionist API",
    version="1.0.0",
    description="Backend API for the AI Receptionist project."
)
#This defines a GET endpoint for the root URL.
@app.get("/")
def root():
    return {
         "message": "Welcome to the AI Receptionist API!"
    }

# Endpoint used to verify that the application is running.
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
    