from datetime import datetime
from app.database.database import initialize_database
from app.database.models import Personality
from app.database.repositories import  PersonalityRepository
def test_personality_repository_create_and_get():
    initialize_database()

    repository = PersonalityRepository()

    personality = Personality(
        personality_id="personality_001",
        name="Default",
        tone="casual",
        formality="low",
        emoji_usage="occasional",
        response_length="short",
        created_at=datetime(2026, 8, 20, 20, 0)
    )

    repository.create(personality)

    stored = repository.get_by_id("personality_001")

    assert stored is not None
    assert stored.name == "Default"
    assert stored.tone == "casual"
    assert stored.formality == "low"
    assert stored.emoji_usage == "occasional"
    assert stored.response_length == "short"


def test_personality_repository_get_all():
    initialize_database()

    repository = PersonalityRepository()

    repository.create(
        Personality(
            personality_id="personality_002",
            name="Casual",
            tone="friendly",
            formality="low",
            emoji_usage="rare",
            response_length="short",
            created_at=datetime(2026, 8, 20, 20, 1)
        )
    )

    repository.create(
        Personality(
            personality_id="personality_003",
            name="Formal",
            tone="professional",
            formality="high",
            emoji_usage="none",
            response_length="medium",
            created_at=datetime(2026, 8, 20, 20, 2)
        )
    )

    personalities = repository.get_all()

    assert len(personalities) == 2


def test_personality_repository_delete():
    initialize_database()

    repository = PersonalityRepository()

    repository.create(
        Personality(
            personality_id="personality_004",
            name="Temporary",
            tone="casual",
            formality="low",
            emoji_usage="occasional",
            response_length="short",
            created_at=datetime(2026, 8, 20, 20, 3)
        )
    )

    repository.delete("personality_004")

    stored = repository.get_by_id("personality_004")

    assert stored is None