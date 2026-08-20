from datetime import datetime
from app.database.models import Person
class PersonManager:
    def __init__(self):
        self._people: dict[str, Person] = {}
    def add_person(
        self,
        person_id: str,
        name: str,
        platform: str
    ) -> Person:
        if person_id in self._people:
            raise ValueError(f"Person already exists: {person_id}")

        person = Person(
            person_id=person_id,
            name=name,
            platform=platform,
            created_at=datetime.now()
        )

        self._people[person_id] = person

        return person

    def get_person(self, person_id: str) -> Person | None:
        return self._people.get(person_id)

    def get_all_people(self) -> list[Person]:
        return list(self._people.values())

    def remove_person(self, person_id: str) -> None:
        if person_id not in self._people:
            raise ValueError(f"Person not found: {person_id}")

        del self._people[person_id]