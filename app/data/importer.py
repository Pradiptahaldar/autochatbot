from pathlib import Path
from pyexpat.errors import messages
from app.data.parser import parse_message
from app.data.cleaner import clean_messages
from app.data.normalizer import normalize_messages
def import_chat(file_path: str) -> list[dict]:
    """
    Read a chat file and convert all valid message lines
    into structured message dictionaries.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Chat file not found: {file_path}")
    messages = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            parsed_message = parse_message(line)

            if parsed_message is not None:
                messages.append(parsed_message)
    return messages
def process_chat(file_path: str) -> list[dict]:
    """
    Run the complete chat data pipeline.
    """

    messages = import_chat(file_path)
    cleaned_messages = clean_messages(messages)
    normalized_messages = normalize_messages(cleaned_messages)

    return normalized_messages