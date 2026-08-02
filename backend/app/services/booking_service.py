
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
                f"Appointment booked successfully for " 
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

    @staticmethod
    def update_appointment(
        appointment_id: int,
        request: BookingRequest,
        db: Session,
    ) -> BookingResponse:
      """
          Update an existing appointment.

      Args:
          appointment_id (int): Appointment ID.
          request (BookingRequest): Updated appointment details.
          db (Session): Database session.

    Returns:
        BookingResponse: Status message.
      """
      # Find one record based on filter criteria. If no record is found , return None.
      # Equivalent SQL: SELECT * FROM appointments WHERE id = appointment_id LIMIT 1;
      appointment = (
          db.query(Appointment)
          .filter(Appointment.id == appointment_id)
          .first()
     )
      if appointment is None:
          return AppointmentResponse(
              status="error",
              message=f"Appointment with ID {appointment_id} not found."
          )

      # Update values
      appointment.customer_name = request.customer_name
      appointment.appointment_date = request.appointment_date
      appointment.appointment_time = request.appointment_time

      db.commit()
      db.refresh(appointment) #Reloads the object from the database to ensure it's synchronized with the latest stored values.

      return BookingResponse(
          status="success",
          message=(
              f"Appointment {appointment.id} updated successfully."
          )
         
      )
