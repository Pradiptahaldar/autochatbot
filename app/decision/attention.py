from dataclasses import dataclass
@dataclass
class AttentionResult:
    should_attention: bool
    reason: str