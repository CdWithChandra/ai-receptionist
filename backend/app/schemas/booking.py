from pydantic import BaseModel

class BookingRequest(BaseModel):
    """
    Represents a booking request with necessary details.
    """
    customer_name: str
    appointment_date:str 
    appointment_time:str

class BookingResponse(BaseModel):
    """
     Represents the response after booking an appointment.
    """
    status: str
    message: str

