from app.ai.booking_agent import BookingAgent
from app.schemas.chat import ChatIntent, ChatResponse
from sqlalchemy.orm import Session
from app.services.booking_service import BookingService
from sqlalchemy.orm import Session
from app.schemas.booking import BookingRequest


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
            return ChatResponse(
                reply="Hello! Welcome to AI Receptionist. How can I help you today?"
            )

        # if detected_intent.intent == "book_appointment":
        #     return ChatResponse(
        #         reply="Sure! I'd be happy to help you book an appointment."
        #     )
        if detected_intent.intent == "book_appointment":
            booking_data = BookingAgent.extract_booking_data(message)
            if(
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
        request = BookingRequest(
            customer_name=booking_data.customer_name,
            appointment_date=booking_data.appointment_date,
            appointment_time=booking_data.appointment_time,
        )
        BookingService.book_appointment(request,db)
        return ChatResponse(
            reply=(
                f"Appointment booked successfully for "
                f"{booking_data.customer_name} on "
                f"{booking_data.appointment_date} at "
                f"{booking_data.appointment_time}."
            )
        )

        if detected_intent.intent == "show_appointments":
            appointments = BookingService.get_appointments(db)
            if not appointments:
                return ChatResponse(
                    reply="There are no appointments scheduled."
                )
            lines = ["Here are your appointments:\n"]
            for appointment in appointments:
                lines.append(
                    f"{appointment.id}"
                    f"{appointment.customer_name}"
                    f"{appointment.appointment_date}"
                    f"{appointment.appointment_time}"
                )
            return ChatResponse(
                reply="\n".join(lines)
            )

        if detected_intent.intent == "update_appointment":
            return ChatResponse(
                reply="I can help you update an appointment."
            )

        if detected_intent.intent == "cancel_appointment":
            return ChatResponse(
                reply="I can help you cancel an appointment."
            )

        return ChatResponse(
            reply="I'm sorry, I didn't understand your request."
        )