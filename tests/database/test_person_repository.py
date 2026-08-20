from datetime import datetime
from app.database.database import initialize_database
from app.database.models import Person
from app.database.repositories import PersonRepository
  
def test_person_repository_create_and_get():
    initialize_database()

    repository = PersonRepository()

    person = Person(
        person_id="test_person_001",
        name="Person A",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 0)
    )

    repository.create(person)

    stored_person = repository.get_by_id("test_person_001")

    assert stored_person is not None
    assert stored_person.person_id == "test_person_001"
    assert stored_person.name == "Person A"
    assert stored_person.platform == "instagram"
def test_person_repository_get_all():
    initialize_database()

    repository = PersonRepository()

    person = Person(
        person_id="test_person_002",
        name="Person B",
        platform="instagram",
        created_at=datetime(2026, 8, 20, 14, 1)
    )
    repository.create(person)
    people = repository.get_all()
    assert any(
        person.person_id == "test_person_002"
        for person in people
    )
def test_person_repository_delete():
    initialize_database()
    repository = PersonRepository()
    person = Person(
        person_id="test_person_003",
        name="Person C",
        platform="whatsapp",
        created_at=datetime(2026, 8, 20, 14, 2)
    )
    repository.create(person)
    repository.delete("test_person_003")
    stored_person = repository.get_by_id("test_person_003")
    assert stored_person is None