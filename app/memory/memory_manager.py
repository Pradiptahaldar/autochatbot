from datetime import datetime
from app.database.models import Memory
from app.database.repositories import MemoryRepository
class MemoryManager:
    def __init__(
        self,
        repository: MemoryRepository | None = None
    ):
        self._repository = repository or MemoryRepository()

    def add_memory(
        self,
        memory_id: str,
        person_id: str,
        content: str,
        memory_type: str,
        importance: float
    ) -> Memory:

        if not 0.0 <= importance <= 1.0:
            raise ValueError(
                "Importance must be between 0.0 and 1.0"
            )

        if self.get_memory(memory_id) is not None:
            raise ValueError(
                f"Memory already exists: {memory_id}"
            )

        memory = Memory(
            memory_id=memory_id,
            person_id=person_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            created_at=datetime.now()
        )

        self._repository.create(memory)

        return memory

    def get_memory(
        self,
        memory_id: str
    ) -> Memory | None:

        return self._repository.get_by_id(memory_id)

    def get_person_memories(
        self,
        person_id: str
    ) -> list[Memory]:

        return self._repository.get_by_person(person_id)

    def remove_memory(
        self,
        memory_id: str
    ) -> None:

        if self.get_memory(memory_id) is None:
            raise ValueError(
                f"Memory not found: {memory_id}"
            )

        self._repository.delete(memory_id)