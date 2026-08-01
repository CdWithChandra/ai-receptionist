from pydantic import BaseModel

class BookingRequest(BaseModel):
    """
    Represents a booking request with necessary details for processing
    """
    customer_name: str
    appointment_date:str 
    appointment_time:str

class BookingResponse(BaseModel):
    """
    Represents a booking response with confirmation details
    """
    status: str
    message: str
    
