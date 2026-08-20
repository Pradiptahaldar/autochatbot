from datetime import datetime
from app.database.models import Conversation
from app.database.repositories import ConversationRepository
class ConversationManager:
    def __init__(
        self,
        repository: ConversationRepository | None = None
    ):
        self._repository = repository or ConversationRepository()
    def create_conversation(
        self,
        conversation_id: str,
        person_id: str,
        platform: str
    ) -> Conversation:
        if self.get_conversation(conversation_id) is not None:
            raise ValueError(
                f"Conversation already exists: {conversation_id}"
            )
        conversation = Conversation(
            conversation_id=conversation_id,
            person_id=person_id,
            platform=platform,
            created_at=datetime.now()
        )
        self._repository.create(conversation)
        return conversation
    def get_conversation(
        self,
        conversation_id: str
    ) -> Conversation | None:

        return self._repository.get_by_id(conversation_id)

    def get_person_conversations(
        self,
        person_id: str
    ) -> list[Conversation]:

        return self._repository.get_by_person(person_id)

    def update_last_message_time(
        self,
        conversation_id: str,
        timestamp: datetime
    ) -> None:

        if self.get_conversation(conversation_id) is None:
            raise ValueError(
                f"Conversation not found: {conversation_id}"
            )

        self._repository.update_last_message_time(
            conversation_id,
            timestamp
        )