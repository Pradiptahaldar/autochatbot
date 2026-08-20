import re
from datetime import datetime


MESSAGE_PATTERN = re.compile(
    r"^\[(?P<timestamp>[\d-]+\s[\d:]+)\]\s(?P<sender>[^:]+):\s(?P<text>.*)$"
)


def parse_message(line: str) -> dict | None:
    """
    Parse one chat message line into structured data.
    Expected format:
    [YYYY-MM-DD HH:MM] Sender: message
    """

    match = MESSAGE_PATTERN.match(line.strip())

    if not match:
        return None

    timestamp = datetime.strptime(
        match.group("timestamp"),
        "%Y-%m-%d %H:%M"
    )

    return {
        "timestamp": timestamp.isoformat(),
        "sender": match.group("sender").strip(),
        "text": match.group("text").strip(),
    }