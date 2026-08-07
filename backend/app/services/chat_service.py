from sqlalchemy.orm import Session

from app.ai.booking_agent import BookingAgent
from app.schemas.booking import BookingRequest
from app.schemas.chat import ChatIntent, ChatResponse
from app.services.booking_service import BookingService
from app.services.conversation_manager import ConversationManager
from app.services.ai_service import AIService


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    @staticmethod
    def get_response(message: str, db: Session) -> ChatResponse:
        """
        Generate a response based on the detected intent.
        """
        state =ConversationManager.get_state()

        # Continue an existing booking conversation
        if (
            state["intent"]=="book_appointment"
            and state["waiting_for"] == "customer_name"
        ):
            ConversationManager.update_state(
                customer_name = message.strip(),
                waiting_for = "appointment_date",
            ) 
            return ChatResponse (
                reply="What appointment date would you like? (YYYY-MM-DD)"
            )
        if (
            state["intent"] == "book_appointment"
            and state["waiting_for"] == "appointment_date"
        ):
            ConversationManager.update_state(
                appointment_date = message.strip(),
                waiting_for="appointment_time",
            )
            return ChatResponse(
                reply="What appointment time would you like? (e.g., 10:30 AM)"     
         )

        if (
            state["intent"] == "book_appointment"
            and state["waiting_for"] == "appointment_time"
        ):
            ConversationManager.update_state(
                appointment_time = message.strip(),
            )
            state = ConversationManager.get_state()

            request = BookingRequest(
                 customer_name=state["customer_name"],
                 appointment_date=state["appointment_date"],
                 appointment_time=state["appointment_time"],
            )

            BookingService.book_appointment(request,db)
            ConversationManager.clear_state()

            return ChatResponse(
                reply=(
                    f"Appointment booked successfully for "
                    f"{request.customer_name} on "
                    f"{request.appointment_date} at "
                    f"{request.appointment_time}."
                )
            )
        
        detected_intent: ChatIntent = BookingAgent.process_message(message)

        if detected_intent.intent == "empty":
            return ChatResponse(
                reply="Please enter a valid message."
            )

        if detected_intent.intent == "greeting":
            return ChatService._handle_greeting()

        if detected_intent.intent == "book_appointment":
            return ChatService._handle_booking(message, db)

        if detected_intent.intent == "show_appointments":
            return ChatService._handle_show_appointments(db)

        if detected_intent.intent == "update_appointment":
            return ChatService._handle_update(message, db)
        
        if detected_intent.intent == "cancel_appointment":
            return ChatService._handle_cancel(message, db)

        return AIService.get_ai_response(message)

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
        state = ConversationManager.get_state()
        booking_data = BookingAgent.extract_booking_data(message)
        if (
            booking_data.customer_name is None 
            and booking_data.appointment_date is None
            and booking_data.appointment_time is None
        ):
            ConversationManager.update_state(
                intent="book_appointment",
                waiting_for="customer_name",
            )
            return ChatResponse(
                reply="Sure! What's the customer's name?"
            )
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
        request = BookingRequest(
            customer_name = booking_data.customer_name,
            appointment_date = booking_data.appointment_date,
            appointment_time = booking_data.appointment_time
        )
        result = BookingService.book_appointment(
            request,db
        )
        ConversationManager.clear_state()
        return ChatResponse(
            reply=result.message
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
             or update_data.customer_name is None
             or update_data.appointment_date is None
             or update_data.appointment_time is None
         ):
             return ChatResponse (
                 reply= (
                     "Please provide the appointment ID, "
                     "customer name, new date (YYYY-MM-DD), "
                     "and new time."
                 )
             )
         request= BookingRequest(
             customer_name=update_data.customer_name,
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
                 f"appointment {update_data.appointment_id} updated successfully "
                 f"for {update_data.customer_name} on "
                 f"{update_data.appointment_date} at "
                 f"{update_data.appointment_time}."
             )
         )

    @staticmethod
    def _handle_cancel(
        messsage: str,
        db: Session
    ) -> ChatResponse:
        """
        Handle cancel appointment requclearests.
        """

        cancel_data = BookingAgent.extract_cancel_data(messsage)
        if cancel_data.appointment_id is None:
            return ChatResponse(
                reply="Please provide the appointment ID."
            )
        result = BookingService.delete_appointment(
            cancel_data.appointment_id,
            db
        )

        if result.status=="error":
            return ChatResponse(
                reply=result.message
            )
        
        return ChatResponse(
            reply=(
                f"Appointment {cancel_data.appointment_id} "
                f" has been cancelled successfully."
            )
        )

    @staticmethod
    def _handle_unknown() -> ChatResponse:
        """
        Handle unknown requests.
        """
        return ChatResponse(
            reply= "I'm sorry, I didn't understand your request."
        )


