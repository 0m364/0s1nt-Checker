import pytest
from app.schemas import PersonSearch

@pytest.fixture
def person_search():
    return PersonSearch(
        full_name="John Doe",
        dob="1990-01-01",
        address="123 Main St",
        email="john@example.com",
        phone="555-0123"
    )
