from sqlalchemy.orm import Session

from app.ai.booking_agent import BookingAgent
from app.schemas.booking import BookingRequest
from app.schemas.chat import ChatIntent, ChatResponse
from app.services.booking_service import BookingService


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    @staticmethod
    def get_response(message: str, db: Session) -> ChatResponse:
        """
        Generate a response based on the detected intent.
        """

        detected_intent: ChatIntent = BookingAgent.process_message(message)

        if detected_intent.intent == "empty":
            return ChatResponse(
                reply="Please enter a valid message."
            )

        if detected_intent.intent == "greeting":
            return ChatService._handle_greeting()

        if detected_intent.intent == "book_appointment":
            return ChatService._handle_booking(message,db)

        if detected_intent.intent == "show_appointments":
            return ChatService._handle_show_appointments(db)

        if detected_intent.intent == "update_appointment":
            return ChatService._handle_update(message,db)
        
        if detected_intent.intent == "cancel_appointment":
            return ChatService._handle_cancel()

        return ChatService._handle_unknown()

    @staticmethod
    def _handle_greeting() -> ChatResponse:
        """
        Handle greeting messages.
        """
        return ChatResponse(
            reply="Hello! Welcome to AI Receptionist. How can I help you today?"
        )
    
    @staticmethod
    def _handle_booking(
        message: str,
        db: Session,       
    ) -> ChatResponse:
        """
        Handle appointment booking requests.
        """
        booking_data = BookingAgent.extract_booking_data(message)
        if (
            booking_data.customer_name is None 
            or booking_data.appointment_date is None
            or booking_data.appointment_time is None
        ):
            return ChatResponse(
                reply=(
                    "Please provide the customer's name, "
                    "appointment date (YYYY-MM-DD), "
                    "and appointment time."
                )
            )
        request =BookingRequest (
            customer_name=booking_data.customer_name,
            appointment_date=booking_data.appointment_date,
            appointment_time=booking_data.appointment_time
        )
        BookingService.book_appointment(request,db)
        return ChatResponse(
            reply=(
                f"Appointment booked successfully for "
                f"{booking_data.customer_name}"
                f"{booking_data.appointment_date}"
                f"{booking_data.appointment_time}"
            )
        )
    
    @staticmethod
    def _handle_show_appointments(
            db: Session
    ) -> ChatResponse:
        """
        Handle requests to view appointments.
        """
        appointments = BookingService.get_appointments(db)
        if not appointments:
            return ChatResponse(
                reply="There are no appointments scheduled."
            )
        lines = ["Here are your appointments:\n"]
        for appointment in appointments:
            lines.append(
                f"{appointment.id}. "
                f"{appointment.customer_name} - "
                f"{appointment.appointment_date} - "
                f"{appointment.appointment_time}"
            )
        return ChatResponse(
            reply="\n".join(lines)
        )
    @staticmethod
    def _handle_update(message: str,
                       db: Session) -> ChatResponse:
         """
         Handle update appointment requests.
         """
         update_data = BookingAgent.extract_update_data(message)
         if (
             update_data.appointment_id is None
             or update_data.appointment_date is None
             or update_data.appointment_time is None
         ):
             return ChatResponse (
                 reply= (
                     "Please provide the appointment ID, "
                     "new date (YYYY-MM-DD), "
                     "and new time."
                 )
             )
         request= BookingRequest(
             customer_name="", # Placeholder for now
             appointment_date=update_data.appointment_date,
             appointment_time=update_data.appointment_time,
         )

         result = BookingService.update_appointment(
             update_data.appointment_id,
             request,
             db
         )
         if result.status== "error":
             return ChatResponse(
                 reply=result.message
             )

         return ChatResponse(
             reply=(
                 f"appointment {update_data.appointment_id} updated "
                 f"to {update_data.appointment_date} to "
                 f"{update_data.appointment_time}."
             )
         )

    @staticmethod
    def _handle_cancel() -> ChatResponse:
        """
        Handle cancel appointment requclearests.
        """
        return ChatResponse(
            reply="I can help you cancel an appointment."
        )

    @staticmethod
    def _handle_unknown() -> ChatResponse:
        """
        Handle unknown requests.
        """
        return ChatResponse(
            reply= "I'm sorry, I didn't understand your request."
        )


