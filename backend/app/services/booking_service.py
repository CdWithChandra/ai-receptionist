from app.schemas.booking import BookingRequest

class BookingService:
    """
    Service class for appointment booking operations.
    """

    def book_appointment(request: BookingRequest) -> dict:
        """
        Simulate booking an appointment.

        Args:
            request (BookingRequest): Appointment details.

        Returns:
            dict: Booking confirmation.
        """
        return {
            "status": "success",
            "message": f"Appointment booked successfully for"
            f"{request.customer_name} on "
            f"{request.appointment_date} at "
            f"{request.appointment_time}"
        }