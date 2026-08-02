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

class ChatIntent(BaseModel):
    """
    Represents the intent detected by the AI agent.
    """
    intent: str