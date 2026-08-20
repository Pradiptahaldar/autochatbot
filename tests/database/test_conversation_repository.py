from app.database.models import Person, Conversation
from app.database.repositories import PersonRepository, ConversationRepository
from app.database.database import  initialize_database
from datetime import datetime

def test_conversation_repository_create_and_get():
    initialize_database()

    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()

    person = Person(
        person_id="conversation_person_001",
        name="Person A",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 10)
    )

    person_repository.create(person)

    conversation = Conversation(
        conversation_id="conversation_001",
        person_id="conversation_person_001",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 11)
    )

    conversation_repository.create(conversation)

    stored = conversation_repository.get_by_id(
        "conversation_001"
    )

    assert stored is not None
    assert stored.conversation_id == "conversation_001"
    assert stored.person_id == "conversation_person_001"


def test_conversation_repository_get_by_person():
    initialize_database()

    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()

    person = Person(
        person_id="conversation_person_002",
        name="Person B",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 12)
    )

    person_repository.create(person)

    conversation_repository.create(
        Conversation(
            conversation_id="conversation_002",
            person_id="conversation_person_002",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 14, 13)
        )
    )

    conversation_repository.create(
        Conversation(
            conversation_id="conversation_003",
            person_id="conversation_person_002",
            platform="whatsapp",
            created_at=datetime(2026, 8, 20, 14, 14)
        )
    )

    conversations = conversation_repository.get_by_person(
        "conversation_person_002"
    )

    assert len(conversations) == 2


def test_conversation_repository_update_last_message_time():
    initialize_database()

    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()

    person_repository.create(
        Person(
            person_id="conversation_person_003",
            name="Person C",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 14, 15)
        )
    )

    conversation_repository.create(
        Conversation(
            conversation_id="conversation_004",
            person_id="conversation_person_003",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 14, 16)
        )
    )

    timestamp = datetime(2026, 8, 20, 15, 0)

    conversation_repository.update_last_message_time(
        "conversation_004",
        timestamp
    )

    stored = conversation_repository.get_by_id(
        "conversation_004"
    )

    assert stored is not None
    assert stored.last_message_at == timestamp