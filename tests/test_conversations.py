from datetime import datetime
from app.conversations.conversation_manager import ConversationManager
from app.conversations.person_manager import PersonManager
from app.conversations.message_manager import MessageManager
def test_add_person():
    manager = PersonManager()
    person = manager.add_person(
        person_id="person_001",
        name="Person A",
        platform="instagram"
    )

    assert person.person_id == "person_001"
    assert person.name == "Person A"
    assert person.platform == "instagram"
def test_get_person():
    manager = PersonManager()

    manager.add_person(
        person_id="person_001",
        name="Person A",
        platform="instagram"
    )

    person = manager.get_person("person_001")

    assert person is not None
    assert person.name == "Person A"
def test_get_all_people():
    manager = PersonManager()

    manager.add_person(
        person_id="person_001",
        name="Person A",
        platform="instagram"
    )

    manager.add_person(
        person_id="person_002",
        name="Person B",
        platform="whatsapp"
    )
    people = manager.get_all_people()
    assert len(people) == 2
def test_remove_person():
    manager = PersonManager()
    manager.add_person(
        person_id="person_001",
        name="Person A",
        platform="instagram"
    )
    manager.remove_person("person_001")
    assert manager.get_person("person_001") is None

def test_create_conversation():
    manager = ConversationManager()

    conversation = manager.create_conversation(
        conversation_id="conv_001",
        person_id="person_001",
        platform="instagram"
    )
    assert conversation.conversation_id == "conv_001"
    assert conversation.person_id == "person_001"
    assert conversation.platform == "instagram"
def test_get_conversation():
    manager = ConversationManager()

    manager.create_conversation(
        conversation_id="conv_001",
        person_id="person_001",
        platform="instagram"
    )

    conversation = manager.get_conversation("conv_001")

    assert conversation is not None
    assert conversation.person_id == "person_001"


def test_get_person_conversations():
    manager = ConversationManager()

    manager.create_conversation(
        conversation_id="conv_001",
        person_id="person_001",
        platform="instagram"
    )

    manager.create_conversation(
        conversation_id="conv_002",
        person_id="person_001",
        platform="whatsapp"
    )

    manager.create_conversation(
        conversation_id="conv_003",
        person_id="person_002",
        platform="instagram"
    )

    conversations = manager.get_person_conversations("person_001")

    assert len(conversations) == 2


def test_update_last_message_time():
    manager = ConversationManager()

    manager.create_conversation(
        conversation_id="conv_001",
        person_id="person_001",
        platform="instagram"
    )

    timestamp = datetime(2026, 8, 20, 13, 0)

    manager.update_last_message_time(
        "conv_001",
        timestamp
    )

    conversation = manager.get_conversation("conv_001")

    assert conversation is not None
    assert conversation.last_message_at == timestamp

def test_add_message():
    manager = MessageManager()

    message = manager.add_message(
        message_id="msg_001",
        conversation_id="conv_001",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 13, 0),
        text="hello"
    )

    assert message.message_id == "msg_001"
    assert message.conversation_id == "conv_001"
    assert message.sender == "Person A"
    assert message.text == "hello"


def test_get_message():
    manager = MessageManager()

    manager.add_message(
        message_id="msg_001",
        conversation_id="conv_001",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 13, 0),
        text="hello"
    )

    message = manager.get_message("msg_001")

    assert message is not None
    assert message.text == "hello"


def test_get_conversation_messages():
    manager = MessageManager()

    manager.add_message(
        message_id="msg_002",
        conversation_id="conv_001",
        sender="Me",
        timestamp=datetime(2026, 8, 20, 13, 2),
        text="I'm coming"
    )

    manager.add_message(
        message_id="msg_001",
        conversation_id="conv_001",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 13, 1),
        text="where are you?"
    )

    manager.add_message(
        message_id="msg_003",
        conversation_id="conv_002",
        sender="Person B",
        timestamp=datetime(2026, 8, 20, 13, 3),
        text="hello"
    )

    messages = manager.get_conversation_messages("conv_001")

    assert len(messages) == 2
    assert messages[0].message_id == "msg_001"
    assert messages[1].message_id == "msg_002"


def test_remove_message():
    manager = MessageManager()

    manager.add_message(
        message_id="msg_001",
        conversation_id="conv_001",
        sender="Person A",
        timestamp=datetime(2026, 8, 20, 13, 0),
        text="hello"
    )

    manager.remove_message("msg_001")

    assert manager.get_message("msg_001") is None