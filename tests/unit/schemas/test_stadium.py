import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.repositories.stadiumRepository import StadiumRepository
from app.schemas.stadium import Stadium

@pytest.fixture
def in_memory_engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def stadium_repo(in_memory_engine):
    repo = StadiumRepository()
    repo.engine = in_memory_engine
    return repo

class TestStadium:

    def test_create_stadium_with_all_fields_success(self):
        stadium = Stadium(
            id=1,
            name="Maracana",
            city="Rio de Janeiro",
            country_id=1,
            capacity=78838
        )
        assert stadium.id == 1
        assert stadium.name == "Maracana"
        assert stadium.city == "Rio de Janeiro"
        assert stadium.country_id == 1
        assert stadium.capacity == 78838

    def test_create_stadium_with_required_fields_only(self):
        stadium = Stadium(
            name="Allianz Parque",
            country_id=1
        )
        assert stadium.name == "Allianz Parque"
        assert stadium.country_id == 1
        assert stadium.city is None
        assert stadium.capacity is None

    def test_stadium_name_max_length(self):
        name = "A" * 100
        stadium = Stadium(name=name, country_id=1)
        assert stadium.name == name

    def test_stadium_name_exceeds_max_length(self):
        name = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            Stadium(name=name, country_id=1)
        assert "Stadium name cannot exceed 100 characters" in str(exc_info.value)

    def test_stadium_city_max_length(self):
        city = "B" * 100
        stadium = Stadium(name="Arena Teste", country_id=1, city=city)
        assert stadium.city == city

    def test_stadium_city_exceeds_max_length(self):
        city = "B" * 101
        with pytest.raises(ValueError) as exc_info:
            Stadium(name="Arena Teste", country_id=1, city=city)
        assert "Stadium city cannot exceed 100 characters" in str(exc_info.value)

    def test_stadium_name_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Stadium(name=None, country_id=1)
        assert "Stadium name is required" in str(exc_info.value)

    def test_stadium_country_id_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Stadium(name="Arena da Baixada", country_id=None)
        assert "Country ID is required" in str(exc_info.value)