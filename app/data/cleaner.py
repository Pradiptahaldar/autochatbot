def clean_messages(messages: list[dict]) -> list[dict]:
    """
    Clean and validate parsed chat messages.
    """
    cleaned_messages = []
    for message in messages:
        text = message.get("text", "").strip()
        sender = message.get("sender", "").strip()
        if not text or not sender:
            continue
        cleaned_message = {
            "timestamp": message["timestamp"],
            "sender": sender,
            "text": text,
        }
        cleaned_messages.append(cleaned_message)
    return cleaned_messages