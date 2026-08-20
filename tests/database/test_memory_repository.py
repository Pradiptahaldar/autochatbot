from datetime import datetime
from app.database.database import  initialize_database
from app.database.models import Person, Memory
from app.database.repositories import PersonRepository, MemoryRepository
def test_memory_repository_create_and_get():
    initialize_database()

    person_repository = PersonRepository()
    memory_repository = MemoryRepository()

    person_repository.create(
        Person(
            person_id="memory_person_001",
            name="Person A",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 16, 0)
        )
    )

    memory = Memory(
        memory_id="memory_001",
        person_id="memory_person_001",
        content="Person A likes programming.",
        memory_type="preference",
        importance=0.8,
        created_at=datetime(2026, 8, 20, 16, 1)
    )

    memory_repository.create(memory)

    stored = memory_repository.get_by_id("memory_001")

    assert stored is not None
    assert stored.person_id == "memory_person_001"
    assert stored.content == "Person A likes programming."
    assert stored.memory_type == "preference"
    assert stored.importance == 0.8


def test_memory_repository_get_by_person():
    initialize_database()

    person_repository = PersonRepository()
    memory_repository = MemoryRepository()

    person_repository.create(
        Person(
            person_id="memory_person_002",
            name="Person B",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 16, 2)
        )
    )

    memory_repository.create(
        Memory(
            memory_id="memory_002",
            person_id="memory_person_002",
            content="Less important memory.",
            memory_type="topic",
            importance=0.4,
            created_at=datetime(2026, 8, 20, 16, 3)
        )
    )

    memory_repository.create(
        Memory(
            memory_id="memory_003",
            person_id="memory_person_002",
            content="Important memory.",
            memory_type="fact",
            importance=0.9,
            created_at=datetime(2026, 8, 20, 16, 4)
        )
    )

    memories = memory_repository.get_by_person(
        "memory_person_002"
    )

    assert len(memories) == 2
    assert memories[0].importance == 0.9
    assert memories[1].importance == 0.4


def test_memory_repository_delete():
    initialize_database()

    person_repository = PersonRepository()
    memory_repository = MemoryRepository()

    person_repository.create(
        Person(
            person_id="memory_person_003",
            name="Person C",
            platform="whatsapp",
            created_at=datetime(2026, 8, 20, 16, 5)
        )
    )

    memory_repository.create(
        Memory(
            memory_id="memory_004",
            person_id="memory_person_003",
            content="Temporary memory.",
            memory_type="event",
            importance=0.5,
            created_at=datetime(2026, 8, 20, 16, 6)
        )
    )
    memory_repository.delete("memory_004")
    stored = memory_repository.get_by_id("memory_004")
    assert stored is None