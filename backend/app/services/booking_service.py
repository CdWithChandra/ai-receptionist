
from sqlalchemy.orm import Session
from app.database.models.appointment import Appointment
from app.schemas.booking import (AppointmentResponse,BookingRequest, BookingResponse)
from sqlalchemy.orm import Session

class BookingService:
    """
    Service class for appointment booking operations.
    """
    @staticmethod
    def book_appointment(
        request: BookingRequest,
        db: Session) -> BookingResponse:
        """
       Save an appointment to the database. 

        Args:
            request (BookingRequest): Appointment details.
            db (Session): Database session.

        Returns:
            BookingResponse: Booking confirmation.
        """

        appointment = Appointment(
            customer_name=request.customer_name,
            appointment_date=request.appointment_date,
            appointment_time=request.appointment_time
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)


        return BookingResponse(
            status="success",
            message=(
                f"Appointment booked successfully for" 
                f"{request.customer_name} on "
                f"{request.appointment_date} at "
                f"{request.appointment_time} "
                )
        )

    @staticmethod
    def get_appointments(
        db: Session,
    ) -> list[AppointmentResponse]:
        """
        Retrieve all appointments from the database.

        Args:
          db (Session): Database session.

        Returns:
         list[AppointmentResponse]: List of appointments.
        """
        appointments = db.query(Appointment).all()
        return appointments
 