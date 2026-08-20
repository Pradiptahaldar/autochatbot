from datetime import datetime
from app.conversations.person_manager import PersonManager
from app.conversations.conversation_manager import ConversationManager
from app.conversations.message_manager import MessageManager
from app.database.database import get_connection, initialize_database
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
        assert "memories" in table_names
        assert "personalities" in table_names

    finally:
        connection.close()