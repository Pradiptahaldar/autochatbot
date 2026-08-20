from datetime import datetime
from app.database.models import Message
from app.database.repositories import MessageRepository
class MessageManager:
    def __init__(
        self,
        repository: MessageRepository | None = None
    ):
        self._repository = repository or MessageRepository()
    def add_message(
        self,
        message_id: str,
        conversation_id: str,
        sender: str,
        timestamp: datetime,
        text: str
    ) -> Message:

        if self.get_message(message_id) is not None:
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

        self._repository.create(message)

        return message

    def get_message(
        self,
        message_id: str
    ) -> Message | None:

        return self._repository.get_by_id(message_id)

    def get_conversation_messages(
        self,
        conversation_id: str
    ) -> list[Message]:

        return self._repository.get_by_conversation(
            conversation_id
        )

    def remove_message(
        self,
        message_id: str
    ) -> None:

        if self.get_message(message_id) is None:
            raise ValueError(
                f"Message not found: {message_id}"
            )

        self._repository.delete(message_id)