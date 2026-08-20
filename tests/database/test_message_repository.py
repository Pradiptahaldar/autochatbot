from datetime import datetime
from app.database.database import  initialize_database
from app.database.models import Person, Conversation, Message
from app.database.repositories import PersonRepository, ConversationRepository, MessageRepository
def test_message_repository_create_and_get():
    initialize_database()

    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()

    person_repository.create(
        Person(
            person_id="message_person_001",
            name="Person A",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 15, 0)
        )
    )

    conversation_repository.create(
        Conversation(
            conversation_id="message_conversation_001",
            person_id="message_person_001",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 15, 1)
        )
    )

    message = Message(
        message_id="message_001",
        conversation_id="message_conversation_001",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 15, 2),
        text="Hello"
    )

    message_repository.create(message)

    stored = message_repository.get_by_id("message_001")

    assert stored is not None
    assert stored.message_id == "message_001"
    assert stored.conversation_id == "message_conversation_001"
    assert stored.text == "Hello"


def test_message_repository_get_by_conversation():
    initialize_database()

    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()

    person_repository.create(
        Person(
            person_id="message_person_002",
            name="Person B",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 15, 3)
        )
    )

    conversation_repository.create(
        Conversation(
            conversation_id="message_conversation_002",
            person_id="message_person_002",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 15, 4)
        )
    )

    message_repository.create(
        Message(
            message_id="message_002",
            conversation_id="message_conversation_002",
            sender="Person B",
            timestamp=datetime(2026, 8, 20, 15, 5),
            text="First"
        )
    )

    message_repository.create(
        Message(
            message_id="message_003",
            conversation_id="message_conversation_002",
            sender="Me",
            timestamp=datetime(2026, 8, 20, 15, 6),
            text="Second"
        )
    )
    messages = message_repository.get_by_conversation(
        "message_conversation_002"
    )
    assert len(messages) == 2
    assert messages[0].text == "First"
    assert messages[1].text == "Second"
def test_message_repository_delete():
    initialize_database()
    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()
    person_repository.create(
        Person(
            person_id="message_person_003",
            name="Person C",
            platform="whatsapp",
            created_at=datetime(2026, 8, 20, 15, 7)
        )
    )
    conversation_repository.create(
        Conversation(
            conversation_id="message_conversation_003",
            person_id="message_person_003",
            platform="whatsapp",
            created_at=datetime(2026, 8, 20, 15, 8)
        )
    )
    message_repository.create(
        Message(
            message_id="message_004",
            conversation_id="message_conversation_003",
            sender="Person C",
            timestamp=datetime(2026, 8, 20, 15, 9),
            text="Hello"
        )
    )
    message_repository.delete("message_004")
    stored = message_repository.get_by_id("message_004")
    assert stored is None