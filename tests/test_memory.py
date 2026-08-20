import pytest
from datetime import datetime
from app.database.models import Person, Conversation, Message
from app.database.repositories import PersonRepository, ConversationRepository, MessageRepository
from app.memory.short_term import ShortTermMemory
from app.database.database import get_connection, initialize_database
from app.memory.memory_manager import MemoryManager
from app.memory.long_term import LongTermMemory
from app.memory.retrieval import MemoryRetriever
@pytest.fixture(autouse=True)
def clean_database():
    initialize_database()

    connection = get_connection()

    try:
        connection.execute("DELETE FROM memories")
        connection.execute("DELETE FROM messages")
        connection.execute("DELETE FROM conversations")
        connection.execute("DELETE FROM people")
        connection.commit()
    finally:
        connection.close()
def test_add_memory():
    manager = MemoryManager()

    memory = manager.add_memory(
        memory_id="memory_manager_001",
        person_id="person_001",
        content="Person A likes programming.",
        memory_type="preference",
        importance=0.8
    )
    assert memory.memory_id == "memory_manager_001"
    assert memory.person_id == "person_001"
    assert memory.content == "Person A likes programming."
    assert memory.memory_type == "preference"
    assert memory.importance == 0.8


def test_get_memory():
    manager = MemoryManager()

    manager.add_memory(
        memory_id="memory_manager_002",
        person_id="person_001",
        content="Person A studies computer science.",
        memory_type="fact",
        importance=0.9
    )

    memory = manager.get_memory("memory_manager_002")

    assert memory is not None
    assert memory.content == "Person A studies computer science."


def test_get_person_memories():
    manager = MemoryManager()

    manager.add_memory(
        memory_id="memory_manager_003",
        person_id="person_001",
        content="Memory A",
        memory_type="fact",
        importance=0.7
    )

    manager.add_memory(
        memory_id="memory_manager_004",
        person_id="person_001",
        content="Memory B",
        memory_type="topic",
        importance=0.5
    )
    memories = manager.get_person_memories("person_001")
    assert len(memories) == 2
def test_remove_memory():
    manager = MemoryManager()
    manager.add_memory(
        memory_id="memory_manager_005",
        person_id="person_001",
        content="Temporary memory",
        memory_type="event",
        importance=0.4
    )
    manager.remove_memory("memory_manager_005")
    assert manager.get_memory("memory_manager_005") is None
def test_invalid_importance():
    manager = MemoryManager()
    try:
        manager.add_memory(
            memory_id="memory_manager_006",
            person_id="person_001",
            content="Invalid memory",
            memory_type="fact",
            importance=1.5
        )
        assert False
    except ValueError:
        assert True
def test_get_recent_messages():
    person_repository = PersonRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()
    person_repository.create(
        Person(
            person_id="short_term_person",
            name="Person A",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 17, 0)
        )
    )
    conversation_repository.create(
        Conversation(
            conversation_id="short_term_conversation",
            person_id="short_term_person",
            platform="instagram",
            created_at=datetime(2026, 8, 20, 17, 1)
        )
    )
    for index in range(5):
        message_repository.create(
            Message(
                message_id=f"short_term_message_{index}",
                conversation_id="short_term_conversation",
                sender="Person A",
                timestamp=datetime(
                    2026,
                    8,
                    20,
                    17,
                    index + 2
                ),
                text=f"Message {index}"
            )
        )
    memory = ShortTermMemory(message_repository)
    recent_messages = memory.get_recent_messages(
        "short_term_conversation",
        limit=3
    )
    assert len(recent_messages) == 3
    assert recent_messages[0].text == "Message 2"
    assert recent_messages[1].text == "Message 3"
    assert recent_messages[2].text == "Message 4"
def test_recent_messages_invalid_limit():
    memory = ShortTermMemory()
    try:
        memory.get_recent_messages(
            "conversation_001",
            limit=0
        )
        assert False
    except ValueError:
        assert True
def test_get_long_term_memories():
    memory_manager = MemoryManager()
    memory_manager.add_memory(
        memory_id="long_term_001",
        person_id="person_001",
        content="Important fact",
        memory_type="fact",
        importance=0.9
    )
    memory_manager.add_memory(
        memory_id="long_term_002",
        person_id="person_001",
        content="Less important fact",
        memory_type="fact",
        importance=0.5
    )
    memory_manager.add_memory(
        memory_id="long_term_003",
        person_id="person_002",
        content="Another person's memory",
        memory_type="fact",
        importance=0.8
    )
    long_term = LongTermMemory()
    memories = long_term.get_memories(
        "person_001"
    )
    assert len(memories) == 2
    assert memories[0].importance == 0.9
    assert memories[1].importance == 0.5
def test_get_limited_long_term_memories():
    memory_manager = MemoryManager()
    for index in range(5):
        memory_manager.add_memory(
            memory_id=f"long_term_limit_{index}",
            person_id="person_003",
            content=f"Memory {index}",
            memory_type="topic",
            importance=0.5 + index * 0.1
        )
    long_term = LongTermMemory()
    memories = long_term.get_memories(
        "person_003",
        limit=2
    )
    assert len(memories) == 2
def test_long_term_memory_invalid_limit():
    long_term = LongTermMemory()
    try:
        long_term.get_memories(
            "person_001",
            limit=0
        )
        assert False
    except ValueError:
        assert True
def test_memory_retriever():
    memory_manager = MemoryManager()
    memory_manager.add_memory(
        memory_id="retrieval_memory_001",
        person_id="retrieval_person",
        content="Person likes programming.",
        memory_type="preference",
        importance=0.9
    )
    message_repository = MessageRepository()
    message_repository.create(
        Message(
            message_id="retrieval_message_001",
            conversation_id="retrieval_conversation",
            sender="Person A",
            timestamp=datetime(2026, 8, 20, 18, 0),
            text="What are you doing?"
        )
    )
    retriever = MemoryRetriever()
    context = retriever.get_context(
        person_id="retrieval_person",
        conversation_id="retrieval_conversation"
    )
    assert "recent_messages" in context
    assert "memories" in context
    assert len(context["recent_messages"]) == 1
    assert len(context["memories"]) == 1
    assert (
        context["recent_messages"][0].text
        == "What are you doing?"
    )
    assert (
        context["memories"][0].content
        == "Person likes programming."
    )
def test_memory_retriever_limits():
    memory_manager = MemoryManager()
    for index in range(3):
        memory_manager.add_memory(
            memory_id=f"retrieval_limit_memory_{index}",
            person_id="retrieval_limit_person",
            content=f"Memory {index}",
            memory_type="fact",
            importance=0.5 + index * 0.1
        )
    message_repository = MessageRepository()
    for index in range(4):
        message_repository.create(
            Message(
                message_id=f"retrieval_limit_message_{index}",
                conversation_id="retrieval_limit_conversation",
                sender="Person A",
                timestamp=datetime(
                    2026,
                    8,
                    20,
                    18,
                    index
                ),
                text=f"Message {index}"
            )
        )
    retriever = MemoryRetriever()
    context = retriever.get_context(
        person_id="retrieval_limit_person",
        conversation_id="retrieval_limit_conversation",
        recent_message_limit=2,
        long_term_limit=1
    )
    assert len(context["recent_messages"]) == 2
    assert len(context["memories"]) == 1