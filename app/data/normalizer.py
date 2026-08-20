def normalize_messages(messages: list[dict]) -> list[dict]:
    """
    Convert cleaned messages into the standard internal format.
    """
    normalized_messages = []
    for index, message in enumerate(messages, start=1):
        normalized_messages.append({
            "message_id": f"msg_{index:06d}",
            "timestamp": message["timestamp"],
            "sender": message["sender"],
            "text": message["text"],
        })
    return normalized_messages