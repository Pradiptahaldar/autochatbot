from app.data.parser import  parse_message
from app.data.importer import import_chat, process_chat
from app.data.cleaner import clean_messages
from app.data.normalizer import normalize_messages
def test_parse_message():
    line = "[2026-08-20 10:00] Person A: bro where are you"
    result = parse_message(line)
    assert result is not None
    assert result["sender"] == "Person A"
    assert result["text"] == "bro where are you"
    assert result["timestamp"] == "2026-08-20T10:00:00"
def test_import_chat():
    messages = import_chat("data/raw/test_chat.txt")
    assert len(messages) == 6
    assert messages[0]["sender"] == "Person A"
    assert messages[0]["text"] == "bro where are you"
    assert messages[-1]["sender"] == "Me"
def test_clean_messages():
    messages = [
        {
            "timestamp": "2026-08-20T10:00:00",
            "sender": "Person A",
            "text": "  hello  "
        },
        {
            "timestamp": "2026-08-20T10:01:00",
            "sender": "Person A",
            "text": "   "
        },
        {
            "timestamp": "2026-08-20T10:02:00",
            "sender": "  Me  ",
            "text": "  coming bro   "
        }
    ]

    cleaned = clean_messages(messages)

    assert len(cleaned) == 2
    assert cleaned[0]["text"] == "hello"
    assert cleaned[1]["sender"] == "Me"
    assert cleaned[1]["text"] == "coming bro"
def test_normalize_messages():
    messages = [
        {
            "timestamp": "2026-08-20T10:00:00",
            "sender": "Person A",
            "text": "bro where are you"
        },
        {
            "timestamp": "2026-08-20T10:01:00",
            "sender": "Me",
            "text": "coming bro"
        }
    ]
    normalized = normalize_messages(messages)
    assert len(normalized) == 2
    assert normalized[0]["message_id"] == "msg_000001"
    assert normalized[1]["message_id"] == "msg_000002"
    assert normalized[0]["sender"] == "Person A"
    assert normalized[1]["text"] == "coming bro"
def test_process_chat():
    messages = process_chat("data/raw/test_chat.txt")

    assert len(messages) == 6

    assert messages[0]["message_id"] == "msg_000001"
    assert messages[0]["sender"] == "Person A"
    assert messages[0]["text"] == "bro where are you"

    assert messages[-1]["message_id"] == "msg_000006"
    assert messages[-1]["sender"] == "Me"
    assert messages[-1]["text"] == "yeah probably, I'll let you know"