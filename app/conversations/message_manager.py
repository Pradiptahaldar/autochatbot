from datetime import datetime
from app.database.models import Message
class MessageManager:
    def __init__(self):
        self._messages: dict[str, Message] = {}
    def add_message(
        self,
        message_id: str,
        conversation_id: str,
        sender: str,
        timestamp: datetime,
        text: str
    ) -> Message:

        if message_id in self._messages:
            raise ValueError(
                f"Message already exists: {message_id}"
            )

        message = Message(
            message_id=message_id,
            conversation_id=conversation_id,
            sender=sender,
            timestamp=timestamp,
            text=text
        )

        self._messages[message_id] = message

        return message

    def get_message(
        self,
        message_id: str
    ) -> Message | None:

        return self._messages.get(message_id)

    def get_conversation_messages(
        self,
        conversation_id: str
    ) -> list[Message]:

        messages = [
            message
            for message in self._messages.values()
            if message.conversation_id == conversation_id
        ]

        return sorted(
            messages,
            key=lambda message: message.timestamp
        )

    def remove_message(
        self,
        message_id: str
    ) -> None:

        if message_id not in self._messages:
            raise ValueError(
                f"Message not found: {message_id}"
            )

        del self._messages[message_id]