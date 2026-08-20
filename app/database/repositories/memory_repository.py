from datetime import datetime
from app.database.database import get_connection
from app.database.models import Memory
class MemoryRepository:
    def create(self, memory: Memory) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO memories (
                    memory_id,
                    person_id,
                    content,
                    memory_type,
                    importance,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    memory.memory_id,
                    memory.person_id,
                    memory.content,
                    memory.memory_type,
                    memory.importance,
                    memory.created_at.isoformat()
                )
            )

            connection.commit()

        finally:
            connection.close()

    def get_by_id(
        self,
        memory_id: str
    ) -> Memory | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    memory_id,
                    person_id,
                    content,
                    memory_type,
                    importance,
                    created_at
                FROM memories
                WHERE memory_id = ?
                """,
                (memory_id,)
            ).fetchone()

            if row is None:
                return None

            return Memory(
                memory_id=row["memory_id"],
                person_id=row["person_id"],
                content=row["content"],
                memory_type=row["memory_type"],
                importance=row["importance"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                )
            )

        finally:
            connection.close()

    def get_by_person(
        self,
        person_id: str
    ) -> list[Memory]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    memory_id,
                    person_id,
                    content,
                    memory_type,
                    importance,
                    created_at
                FROM memories
                WHERE person_id = ?
                ORDER BY importance DESC, created_at DESC
                """,
                (person_id,)
            ).fetchall()

            return [
                Memory(
                    memory_id=row["memory_id"],
                    person_id=row["person_id"],
                    content=row["content"],
                    memory_type=row["memory_type"],
                    importance=row["importance"],
                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    )
                )
                for row in rows
            ]

        finally:
            connection.close()

    def delete(self, memory_id: str) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                DELETE FROM memories
                WHERE memory_id = ?
                """,
                (memory_id,)
            )

            connection.commit()

        finally:
            connection.close()