from dataclasses import dataclass
@dataclass
class GlobalProfile:
    tone: str
    formality: str
    response_length: str
    emoji_usage: str
    punctuation_style: str
    common_phrases: list[str]