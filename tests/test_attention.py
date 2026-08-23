from app.decision.attention import AttentionResult
def test_attention_result():
    result = AttentionResult(
        should_attention=True,
        reason="message_directed_at_me"
    )
    assert result.should_attention is True
    assert result.reason == "message_directed_at_me"