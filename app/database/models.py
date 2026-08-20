from dataclasses import dataclass
from datetime import datetime
@dataclass
class Person:
    person_id: str
    name: str
    platform: str
    created_at: datetime
@dataclass
class Conversation:
    conversation_id: str
    person_id: str
    platform: str
    created_at: datetime
    last_message_at: datetime | None = None
@dataclass
class Message:
    message_id: str
    conversation_id: str
    sender: str
    text: str
    timestamp: datetime
@dataclass
class Memory:
    memory_id: str
    person_id: str
    content: str
    memory_type: str
    importance: int
    created_at: datetime