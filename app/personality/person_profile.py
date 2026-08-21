from dataclasses import dataclass
@dataclass
class PersonProfile:
    person_id: str
    tone: str
    formality: str
    response_length: str
    emoji_usage: str
    common_phrases: list[str]
    relationship: str