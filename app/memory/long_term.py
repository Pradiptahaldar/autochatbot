from app.database.models import Memory
from app.database.repositories import MemoryRepository
class LongTermMemory:
    def __init__(
        self,
        repository: MemoryRepository | None = None
    ):
        self._repository = repository or MemoryRepository()

    def get_memories(
        self,
        person_id: str,
        limit: int | None = None
    ) -> list[Memory]:

        memories = self._repository.get_by_person(person_id)

        if limit is not None:
            if limit <= 0:
                raise ValueError(
                    "Limit must be greater than zero"
                )

            return memories[:limit]

        return memories