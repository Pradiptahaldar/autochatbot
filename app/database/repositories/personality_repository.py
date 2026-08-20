from datetime import datetime
from app.database.database import get_connection
from app.database.models import Personality
class PersonalityRepository:
    def create(self, personality: Personality) -> None:
        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO personalities (
                    personality_id,
                    name,
                    tone,
                    formality,
                    emoji_usage,
                    response_length,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    personality.personality_id,
                    personality.name,
                    personality.tone,
                    personality.formality,
                    personality.emoji_usage,
                    personality.response_length,
                    personality.created_at.isoformat()
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_by_id(
        self,
        personality_id: str
    ) -> Personality | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    personality_id,
                    name,
                    tone,
                    formality,
                    emoji_usage,
                    response_length,
                    created_at
                FROM personalities
                WHERE personality_id = ?
                """,
                (personality_id,)
            ).fetchone()

            if row is None:
                return None

            return Personality(
                personality_id=row["personality_id"],
                name=row["name"],
                tone=row["tone"],
                formality=row["formality"],
                emoji_usage=row["emoji_usage"],
                response_length=row["response_length"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                )
            )

        finally:
            connection.close()

    def get_all(self) -> list[Personality]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    personality_id,
                    name,
                    tone,
                    formality,
                    emoji_usage,
                    response_length,
                    created_at
                FROM personalities
                ORDER BY created_at
                """
            ).fetchall()

            return [
                Personality(
                    personality_id=row["personality_id"],
                    name=row["name"],
                    tone=row["tone"],
                    formality=row["formality"],
                    emoji_usage=row["emoji_usage"],
                    response_length=row["response_length"],
                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    )
                )
                for row in rows
            ]

        finally:
            connection.close()
    def delete(self, personality_id: str) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                DELETE FROM personalities
                WHERE personality_id = ?
                """,
                (personality_id,)
            )

            connection.commit()
        finally:
            connection.close()