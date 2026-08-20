from datetime import datetime
from app.database.database import get_connection
from app.database.models import Message
class MessageRepository:
    def create(self, message: Message) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO messages (
                    message_id,
                    conversation_id,
                    sender,
                    timestamp,
                    text
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    message.message_id,
                    message.conversation_id,
                    message.sender,
                    message.timestamp.isoformat(),
                    message.text
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_by_id(
        self,
        message_id: str
    ) -> Message | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    message_id,
                    conversation_id,
                    sender,
                    timestamp,
                    text
                FROM messages
                WHERE message_id = ?
                """,
                (message_id,)
            ).fetchone()

            if row is None:
                return None

            return Message(
                message_id=row["message_id"],
                conversation_id=row["conversation_id"],
                sender=row["sender"],
                timestamp=datetime.fromisoformat(
                    row["timestamp"]
                ),
                text=row["text"]
            )

        finally:
            connection.close()

    def get_by_conversation(
        self,
        conversation_id: str
    ) -> list[Message]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    message_id,
                    conversation_id,
                    sender,
                    timestamp,
                    text
                FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp
                """,
                (conversation_id,)
            ).fetchall()

            return [
                Message(
                    message_id=row["message_id"],
                    conversation_id=row["conversation_id"],
                    sender=row["sender"],
                    timestamp=datetime.fromisoformat(
                        row["timestamp"]
                    ),
                    text=row["text"]
                )
                for row in rows
            ]

        finally:
            connection.close()

    def delete(self, message_id: str) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                DELETE FROM messages
                WHERE message_id = ?
                """,
                (message_id,)
            )

            connection.commit()
        finally:
            connection.close()