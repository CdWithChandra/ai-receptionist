# Instead of manually validating JSON, FastAPI does it automatically.
# FastAPI converts it into a ChatRequest object.
# If the client sends invalid data, FastAPI automatically returns a 422 Unprocessable Entity response.

from pydantic import BaseModel

class ChatRequest(BaseModel):
    """ 
    Request model for incoming chat messages.
    """
    message: str

class ChatResponse(BaseModel):
    """
    Response model for outgoing chat messages.
    """
    reply: str