from app.decision.attention import AttentionResult, AttentionAnalyzer
from app.decision.message_classifier import MessageEvent
def test_attention_result():
    result = AttentionResult(
        should_attention=True,
        reason="message_directed_at_me"
    )
    assert result.should_attention is True
    assert result.reason == "message_directed_at_me"
def test_dm_requires_attention():
    analyzer = AttentionAnalyzer()
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="conversation_001",
        conversation_scope="dm"
    )
    result = analyzer.analyze(event)
    assert result.should_attention is True
    assert result.reason == "direct_message"
def test_group_message_directed_at_me_requires_attention():
    analyzer = AttentionAnalyzer()
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="group_001",
        conversation_scope="group",
        target="me"
    )
    result = analyzer.analyze(event)
    assert result.should_attention is True
    assert result.reason == "group_message_directed_at_me"
def test_group_message_for_another_person_does_not_require_attention():
    analyzer = AttentionAnalyzer()

    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="group_001",
        conversation_scope="group",
        target="another_person"
    )
    result = analyzer.analyze(event)
    assert result.should_attention is False
    assert result.reason == "group_message_for_another_person"
def test_group_message_to_everyone_requires_attention():
    analyzer = AttentionAnalyzer()
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="group_001",
        conversation_scope="group",
        target="everyone"
    )
    result = analyzer.analyze(event)
    assert result.should_attention is True
    assert result.reason == "group_message_to_everyone"
def test_group_message_with_unknown_target_requires_attention():
    analyzer = AttentionAnalyzer()
    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="group_001",
        conversation_scope="group",
        target="unknown"
    )
    result = analyzer.analyze(event)
    assert result.should_attention is True
    assert result.reason == "group_message_target_unknown"
def test_community_message_directed_at_me_requires_attention():
    analyzer = AttentionAnalyzer()

    event = MessageEvent(
        content_type="text",
        platform="whatsapp",
        sender_id="person_001",
        conversation_id="community_001",
        conversation_scope="community",
        target="me"
    )

    result = analyzer.analyze(event)

    assert result.should_attention is True
    assert result.reason == "community_message_directed_at_me"