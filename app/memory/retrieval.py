from app.database.models import Memory, Message
from app.memory.long_term import LongTermMemory
from app.memory.short_term import ShortTermMemory
class MemoryRetriever:
    def __init__(
        self,
        short_term: ShortTermMemory | None = None,
        long_term: LongTermMemory | None = None
    ):
        self._short_term = short_term or ShortTermMemory()
        self._long_term = long_term or LongTermMemory()
    def get_context(
        self,
        person_id: str,
        conversation_id: str,
        recent_message_limit: int = 10,
        long_term_limit: int = 10
    ) -> dict[str, list]:
        recent_messages = self._short_term.get_recent_messages(
            conversation_id,
            recent_message_limit
        )
        memories = self._long_term.get_memories(
            person_id,
            long_term_limit
        )
        return {
            "recent_messages": recent_messages,
            "memories": memories
        }