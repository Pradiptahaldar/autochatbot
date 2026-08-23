import pytest
from  app.decision.message_classifier import MessageEvent
def test_message_event_rejects_invalid_content_type():
    with pytest.raises(ValueError):
        MessageEvent(
            content_type ="banana",
            platform= "instagram",
            sender_id="person_001",
            conversation_id="conversation_001"
        )
def test_message_event_rejecs_invalis_paltform():
    with pytest.raises(ValueError):
        MessageEvent(
            content_type="text",
            platform="telegram",
            sender_id="person_001",
            conversation_id="conversation_001"
        )
def test_message_event_can_contain_link():
    event = MessageEvent(
        content_type="text",
        platform="instagram",
        sender_id="peerson_001",
        conversation_id="conversation_001",
        contains_link=True
    )
    assert event.content_type == "text"
    assert event.contains_link is True
def test_link_message_event():
    event = MessageEvent(
        content_type="link",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001"
    )
    assert event.content_type == "link"
    assert event.contains_link is False