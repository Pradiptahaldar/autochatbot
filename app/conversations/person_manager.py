from datetime import datetime
from app.database.models import Person
from app.database.repositories import PersonRepository
class PersonManager:
    def __init__(self, repository: PersonRepository | None = None):
        self._repository = repository or PersonRepository()
    def add_person(
        self,
        person_id: str,
        name: str,
        platform: str
    ) -> Person:
        if self.get_person(person_id) is not None:
            raise ValueError(
                f"Person already exists: {person_id}"
            )

        person = Person(
            person_id=person_id,
            name=name,
            platform=platform,
            created_at=datetime.now()
        )

        self._repository.create(person)

        return person
    def get_person(self, person_id: str) -> Person | None:
        return self._repository.get_by_id(person_id)
    def get_all_people(self) -> list[Person]:
        return self._repository.get_all()
    def remove_person(self, person_id: str) -> None:
        if self.get_person(person_id) is None:
            raise ValueError(
                f"Person not found: {person_id}"
            )
        self._repository.delete(person_id)