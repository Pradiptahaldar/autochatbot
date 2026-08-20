from datetime import datetime
from app.database.models import Conversation
class ConversationManager:
    def __init__(self):
        self._conversations: dict[str, Conversation] = {}
    def create_conversation(
        self,
        conversation_id: str,
        person_id: str,
        platform: str
    ) -> Conversation:
        if conversation_id in self._conversations:
            raise ValueError(
                f"Conversation already exists: {conversation_id}"
            )
        conversation = Conversation(
            conversation_id=conversation_id,
            person_id=person_id,
            platform=platform,
            created_at=datetime.now()
        )
        self._conversations[conversation_id] = conversation
        return conversation
    def get_conversation(
        self,
        conversation_id: str
    ) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def get_person_conversations(
        self,
        person_id: str
    ) -> list[Conversation]:
        return [
            conversation
            for conversation in self._conversations.values()
            if conversation.person_id == person_id
        ]

    def update_last_message_time(
        self,
        conversation_id: str,
        timestamp: datetime
    ) -> None:
        conversation = self.get_conversation(conversation_id)
        if conversation is None:
            raise ValueError(
                f"Conversation not found: {conversation_id}"
            )
        conversation.last_message_at = timestamp