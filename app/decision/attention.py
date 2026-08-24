from dataclasses import dataclass
@dataclass
class AttentionResult:
    should_attention: bool
    reason: str
class AttentionAnalyzer:
    def analyze(self, event):
        if event.conversation_scope == "dm":
            return AttentionResult(
                should_attention=True,
                reason="direct_message"
            )
        if (event.conversation_scope == "group"
            and event.target == "me"
        ):
            return AttentionResult(
                should_attention=True,
                reason="group_message_directed_at_me"
            )
        if (
            event.conversation_scope == "group"
            and event.target == "another_person"
        ):
            return AttentionResult(
                should_attention=False,
                reason="group_message_for_another_person"
            )
        if (
            event.conversation_scope == "group"
            and event.target == "everyone"
        ):
            return AttentionResult(
                should_attention=True,
                reason="group_message_to_everyone"
            )
        if (
            event.conversation_scope == "group"
            and event.target == "unknown"
        ):
            return AttentionResult(
                should_attention=True,
                reason="group_message_target_unknown"
            )
        if (
            event.conversation_scope == "community"
            and event.target == "me"
        ):
            return AttentionResult(
                should_attention=True,
                reason="community_message_directed_at_me"
            )