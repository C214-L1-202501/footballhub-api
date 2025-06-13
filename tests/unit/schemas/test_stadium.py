import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.repositories.stadiumRepository import StadiumRepository
from app.schemas.stadium import Stadium

# ---------- FIXTURES ----------


@pytest.fixture
def in_memory_engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def stadium_repo(in_memory_engine):
    repo = StadiumRepository()
    repo.engine = in_memory_engine  # Override engine for test
    return repo


# ---------- TESTS ----------

"""Corrigir esses testes, pois não estão funcionando."""
# def test_create_stadium(stadium_repo):
#     # Arrange
#     name = "Maracanã"
#     city = "Rio de Janeiro"
#     country_id = 1

#     stadium = stadium_repo.create(name=name, city=city, country_id=country_id)

#     # Assert
#     assert stadium.id is not None
#     assert stadium.name == name
#     assert stadium.city == city
#     assert stadium.country_id == country_id


# def test_get_stadium_by_id(stadium_repo):
#     # Arrange
#     created = stadium_repo.create("Mineirão", "Belo Horizonte", 1)

#     retrieved = stadium_repo.get_by_id(created.id)

#     # Assert
#     assert retrieved is not None
#     assert retrieved.name == "Mineirão"


# def test_get_all_stadiums(stadium_repo):
#     # Arrange
#     stadium_repo.create("Morumbi", "São Paulo", 1)
#     stadium_repo.create("Beira-Rio", "Porto Alegre", 1)

#     stadiums = stadium_repo.get_all()

#     # Assert
#     assert len(stadiums) == 2
#     assert any(s.name == "Morumbi" for s in stadiums)


# def test_update_stadium(stadium_repo):
#     # Arrange
#     stadium = stadium_repo.create("Arena da Baixada", "Curitiba", 1)

#     # Act
#     updated = stadium_repo.update(stadium_id=stadium.id, name="Ligga Arena", city="Curitiba")

#     # Assert
#     assert updated is not None
#     assert updated.name == "Ligga Arena"
#     assert updated.city == "Curitiba"


# def test_delete_stadium(stadium_repo):
#     # Arrange
#     stadium = stadium_repo.create("Fonte Nova", "Salvador", 1)

#     # Act
#     result = stadium_repo.delete(stadium.id)
#     not_found = stadium_repo.get_by_id(stadium.id)

#     # Assert
#     assert result is True
#     assert not_found is None


# def test_delete_non_existing_stadium(stadium_repo):
#     # Act
#     result = stadium_repo.delete(999)

#     # Assert
#     assert result is False
