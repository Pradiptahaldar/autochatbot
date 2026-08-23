from dataclasses import dataclass
VALID_CONTENT_TYPES = {
    "text","image","video","reel",
    "sticker","voice","system","unknown","link"
}
VALID_PLATFORMS = {"instagram","whatsapp"}
@dataclass
class MessageEvent:
    content_type: str
    platform: str
    sender_id: str
    conversation_id: str
    contains_link: bool=False
    def __post_init__(self):
        if self.content_type not in VALID_CONTENT_TYPES:
            raise ValueError(f"unsupporter content type: {self.content_type}")
        if self.platform not in VALID_PLATFORMS:
            raise ValueError(f"unsupported platform:{self.platform}")
        
