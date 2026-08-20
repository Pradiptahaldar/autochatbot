from datetime import datetime
from app.database.database import get_connection
from app.database.models import Conversation
class ConversationRepository:
    def create(self, conversation: Conversation) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO conversations (
                    conversation_id,
                    person_id,
                    platform,
                    created_at,
                    last_message_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    conversation.conversation_id,
                    conversation.person_id,
                    conversation.platform,
                    conversation.created_at.isoformat(),
                    (
                        conversation.last_message_at.isoformat()
                        if conversation.last_message_at
                        else None
                    )
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_by_id(
        self,
        conversation_id: str
    ) -> Conversation | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    conversation_id,
                    person_id,
                    platform,
                    created_at,
                    last_message_at
                FROM conversations
                WHERE conversation_id = ?
                """,
                (conversation_id,)
            ).fetchone()

            if row is None:
                return None

            return Conversation(
                conversation_id=row["conversation_id"],
                person_id=row["person_id"],
                platform=row["platform"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                ),
                last_message_at=(
                    datetime.fromisoformat(row["last_message_at"])
                    if row["last_message_at"]
                    else None
                )
            )

        finally:
            connection.close()

    def get_by_person(
        self,
        person_id: str
    ) -> list[Conversation]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    conversation_id,
                    person_id,
                    platform,
                    created_at,
                    last_message_at
                FROM conversations
                WHERE person_id = ?
                ORDER BY created_at
                """,
                (person_id,)
            ).fetchall()

            return [
                Conversation(
                    conversation_id=row["conversation_id"],
                    person_id=row["person_id"],
                    platform=row["platform"],
                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    ),
                    last_message_at=(
                        datetime.fromisoformat(
                            row["last_message_at"]
                        )
                        if row["last_message_at"]
                        else None
                    )
                )
                for row in rows
            ]

        finally:
            connection.close()

    def update_last_message_time(
        self,
        conversation_id: str,
        timestamp: datetime
    ) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE conversations
                SET last_message_at = ?
                WHERE conversation_id = ?
                """,
                (
                    timestamp.isoformat(),
                    conversation_id
                )
            )
            connection.commit()
        finally:
            connection.close()