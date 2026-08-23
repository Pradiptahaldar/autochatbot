from dataclasses import dataclass
VALID_CONTENT_TYPES = {
    "text","image","video","reel",
    "sticker","voice","system","unknown","link"
}
VALID_PLATFORMS = {"instagram","whatsapp"}
VALID_CONVERSATION_SCOPES = {"dm","group","community",}
VALID_TARGETS = {"me","another_person","everyone","unknown",}
@dataclass
class MessageEvent:
    content_type: str
    platform: str
    sender_id: str
    conversation_id: str
    contains_link: bool=False
    conversation_scope: str = "dm"
    target:str = "unknown"
    reply_to_message_id: str | None = None
    mentioned_user_ids: list[str] | None = None
    def __post_init__(self):
        if self.content_type not in VALID_CONTENT_TYPES:
            raise ValueError(f"unsupporter content type: {self.content_type}")
        if self.platform not in VALID_PLATFORMS:
            raise ValueError(f"unsupported platform:{self.platform}")
        if self.conversation_scope not in VALID_CONVERSATION_SCOPES:
            raise ValueError(
                f"Unsupported conversation scope: "
                f"{self.conversation_scope}"
            )
        if self.target not in VALID_TARGETS:
            raise ValueError(
                f"Unsupported message target: "
                f"{self.target}"
            )
    
        
