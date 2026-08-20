import pytest
from app.database.database import get_connection, initialize_database
@pytest.fixture(autouse=True)
def clean_database():
    initialize_database()
    connection = get_connection()
    try:
        connection.execute("DELETE FROM personalities")
        connection.execute("DELETE FROM messages")
        connection.execute("DELETE FROM memories")
        connection.execute("DELETE FROM conversations")
        connection.execute("DELETE FROM people")
        connection.commit()
    finally:
        connection.close()