import pytest
from datetime import datetime
from app.conversations.person_manager import PersonManager
from app.conversations.conversation_manager import ConversationManager
from app.conversations.message_manager import MessageManager
from app.database.database import get_connection, initialize_database
from app.database.models import Person, Conversation, Message
from app.database.repositories import PersonRepository, ConversationRepository, MessageRepository
@pytest.fixture(autouse=True)
def clean_database():
    initialize_database()
    connection = get_connection()
    try:
        connection.execute("DELETE FROM messages")
        connection.execute("DELETE FROM conversations")
        connection.execute("DELETE FROM people")
        connection.commit()
    finally:
        connection.close()
def test_initialize_database():
    initialize_database()
    connection = get_connection()
    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()
        table_names = [table["name"] for table in tables]
        assert "people" in table_names
        assert "conversations" in table_names
        assert "messages" in table_names

    finally:
        connection.close()
def test_person_repository_create_and_get():
    initialize_database()

    repository = PersonRepository()

    person = Person(
        person_id="test_person_001",
        name="Person A",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 0)
    )

    repository.create(person)

    stored_person = repository.get_by_id("test_person_001")

    assert stored_person is not None
    assert stored_person.person_id == "test_person_001"
    assert stored_person.name == "Person A"
    assert stored_person.platform == "instagram"
def test_person_repository_get_all():
    initialize_database()

    repository = PersonRepository()

    person = Person(
        person_id="test_person_002",
        name="Person B",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 1)
    )
    repository.create(person)
    people = repository.get_all()
    assert any(
        person.person_id == "test_person_002"
        for person in people
    )
def test_person_repository_delete():
    initialize_database()
    repository = PersonRepository()
    person = Person(
        person_id="test_person_003",
        name="Person C",
        platform="whatsapp",
        created_at=datetime(2026, 8, 20, 14, 2)
    )
    repository.create(person)
    repository.delete("test_person_003")
    stored_person = repository.get_by_id("test_person_003")
    assert stored_person is None
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
def test_data_persists_after_manager_recreation():
    person_manager = PersonManager()
    conversation_manager = ConversationManager()
    message_manager = MessageManager()

    person_manager.add_person(
        person_id="persistent_person",
        name="Person A",
        platform="instagram"
    )

    conversation_manager.create_conversation(
        conversation_id="persistent_conversation",
        person_id="persistent_person",
        platform="instagram"
    )

    message_manager.add_message(
        message_id="persistent_message",
        conversation_id="persistent_conversation",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 16, 0),
        text="Hello"
    )

    del person_manager
    del conversation_manager
    del message_manager

    new_person_manager = PersonManager()
    new_conversation_manager = ConversationManager()
    new_message_manager = MessageManager()

    person = new_person_manager.get_person(
        "persistent_person"
    )

    conversation = new_conversation_manager.get_conversation(
        "persistent_conversation"
    )

    messages = new_message_manager.get_conversation_messages(
        "persistent_conversation"
    )

    assert person is not None
    assert person.name == "Person A"

    assert conversation is not None
    assert conversation.person_id == "persistent_person"

    assert len(messages) == 1
    assert messages[0].text == "Hello"    