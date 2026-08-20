from datetime import datetime
from app.database.database import get_connection
from app.database.models import Person
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