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
def test_message_event_has_conversation_scope():
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001",
        conversation_scope="group"
    )
    assert event.conversation_scope == "group"
def test_message_event_rejects_invalid_conversation_scope():
    with pytest.raises(ValueError):
        MessageEvent(
            content_type="text",
            platform="whatsapp",
            sender_id="person_001",
            conversation_id="conversation_001",
            conversation_scope="banana"
        )
def test_message_event_target():
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001",
        conversation_scope="group",
        target="me"
    )
    assert event.target == "me"
def test_message_event_rejects_invalid_target():
    with pytest.raises(ValueError):
        MessageEvent(
            content_type="text",
            platform="whatsapp",
            sender_id="person_001",
            conversation_id="conversation_001",
            target="banana"
        )
def test_message_event_reply_context():
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001",
        reply_to_message_id="message_123"
    )
    assert event.reply_to_message_id == "message_123"
def test_message_event_has_no_reply_by_default():
    event = MessageEvent(
        content_type="text",
        platform="instagram",
        sender_id="person_001",
        conversation_id="conversation_001"
    )
    assert event.reply_to_message_id is None
def test_message_event_mentions_user():
    event = MessageEvent(
        content_type="text",
        platform="instagram",
        sender_id="person_001",
        conversation_id="conversation_001",
        mentioned_user_ids=["user_001"]
    )
    assert event.mentioned_user_ids == ["user_001"]
def test_message_event_has_no_mentions_by_default():
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001"
    )

    assert event.mentioned_user_ids is None