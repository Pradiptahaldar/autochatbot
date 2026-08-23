from app.decision.message_classifier import MessageEvent
def test_message_event():
    event = MessageEvent(
        content_type="text",
        platform="instagram",
        sender_id="person_001",
        conversation_id="conversation_001"
    )
    assert event.content_type == "text"
    assert event.platform == "instagram"
    assert event.sender_id == "person_001"
    assert event.conversation_id == "conversation_001"