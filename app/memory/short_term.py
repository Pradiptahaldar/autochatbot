from app.database.models import Message
from app.database.repositories import MessageRepository
class ShortTermMemory:
    def __init__(
        self,
        repository: MessageRepository | None = None
    ):
        self._repository = repository or MessageRepository()
    def get_recent_messages(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> list[Message]:
        if limit <= 0:
            raise ValueError(
                "Limit must be greater than zero"
            )
        messages = self._repository.get_by_conversation(
            conversation_id
        )
        return messages[-limit:]