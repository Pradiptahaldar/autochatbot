from datetime import datetime
from multiprocessing import connection
from app.database.database import get_connection
from app.database.models import Person, Conversation, Message
class PersonRepository:
    def create(self, person: Person) -> None:
        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO people (
                    person_id,
                    name,
                    platform,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    person.person_id,
                    person.name,
                    person.platform,
                    person.created_at.isoformat()
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_by_id(self, person_id: str) -> Person | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    person_id,
                    name,
                    platform,
                    created_at
                FROM people
                WHERE person_id = ?
                """,
                (person_id,)
            ).fetchone()

            if row is None:
                return None

            return Person(
                person_id=row["person_id"],
                name=row["name"],
                platform=row["platform"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                )
            )

        finally:
            connection.close()

    def get_all(self) -> list[Person]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    person_id,
                    name,
                    platform,
                    created_at
                FROM people
                ORDER BY created_at
                """
            ).fetchall()

            return [
                Person(
                    person_id=row["person_id"],
                    name=row["name"],
                    platform=row["platform"],
                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    )
                )
                for row in rows
            ]

        finally:
            connection.close()

    def delete(self, person_id: str) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                DELETE FROM people
                WHERE person_id = ?
                """,
                (person_id,)
            )
            connection.commit()
        finally:
            connection.close()
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