import pytest
from unittest.mock import MagicMock
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

print(f"DEBUG: Current working directory: {os.getcwd()}")
print(f"DEBUG: DATABASE_URL from os.getenv: {os.getenv('DATABASE_URL')}")

from app.services.ChampionshipService import ChampionshipService
from app.schemas.championship import Championship
from app.schemas.country import Country


@pytest.fixture
def mock_championship_repository():
    return MagicMock()


@pytest.fixture
def championship_service(mock_championship_repository):
    service = ChampionshipService(championship_repository=mock_championship_repository)
    return service


def test_find_championship_by_id_success(championship_service, mock_championship_repository):
    mock_championship = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    mock_championship_repository.get_by_id.return_value = mock_championship

    championship = championship_service.find_championship_by_id(1)

    assert championship == mock_championship
    mock_championship_repository.get_by_id.assert_called_once_with(1)

def test_find_championship_by_id_not_found_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Campeonato não encontrado."):
        championship_service.find_championship_by_id(99)
    mock_championship_repository.get_by_id.assert_called_once_with(99)

def test_find_championship_by_id_repository_exception_is_raised(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.side_effect = Exception("Database connection error")

    with pytest.raises(Exception, match="Database connection error"):
        championship_service.find_championship_by_id(1)
    mock_championship_repository.get_by_id.assert_called_once_with(1)


def test_find_championship_by_name_success(championship_service, mock_championship_repository):
    mock_championship = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    mock_championship_repository.get_by_name.return_value = mock_championship

    championship = championship_service.find_championship_by_name("Brasileirão")

    assert championship == mock_championship
    mock_championship_repository.get_by_name.assert_called_once_with("Brasileirão")

def test_find_championship_by_name_not_found_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_name.return_value = None

    with pytest.raises(ValueError, match="Campeonato não encontrado."):
        championship_service.find_championship_by_name("NonExistentLeague")
    mock_championship_repository.get_by_name.assert_called_once_with("NonExistentLeague")

def test_find_championship_by_name_repository_exception_is_raised(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_name.side_effect = Exception("Network error")

    with pytest.raises(Exception, match="Network error"):
        championship_service.find_championship_by_name("Brasileirão")
    mock_championship_repository.get_by_name.assert_called_once_with("Brasileirão")


def test_create_championship_success(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_name.return_value = None
    new_championship = Championship(id=1, name="New League", country_id=1, type="League", season="2024")
    mock_championship_repository.create.return_value = new_championship

    championship = championship_service.create_championship("New League", 1, "League", "2024")

    assert championship == new_championship
    mock_championship_repository.get_by_name.assert_called_once_with("New League")
    mock_championship_repository.create.assert_called_once_with("New League", 1, "League", "2024")

def test_create_championship_name_empty_raises_value_error(championship_service):
    with pytest.raises(ValueError, match="Championship name cannot be empty."):
        championship_service.create_championship("", 1, "League", "2024")

def test_create_championship_name_not_string_raises_value_error(championship_service):
    with pytest.raises(ValueError, match="Championship name must be a string."):
        championship_service.create_championship(123, 1, "League", "2024")

def test_create_championship_name_too_long_raises_value_error(championship_service):
    with pytest.raises(ValueError, match="Championship name cannot exceed 100 characters."):
        championship_service.create_championship("a" * 101, 1, "League", "2024")

def test_create_championship_name_already_exists_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_name.return_value = Championship(id=1, name="Existing League", country_id=1, type="League", season="2023")

    with pytest.raises(ValueError, match="Championship with this name already exists."):
        championship_service.create_championship("Existing League", 1, "League", "2024")
    mock_championship_repository.get_by_name.assert_called_once_with("Existing League")
    mock_championship_repository.create.assert_not_called()


def test_get_all_championships_success(championship_service, mock_championship_repository):
    mock_championships = [
        Championship(id=1, name="League A", country_id=1, type="League", season="2023"),
        Championship(id=2, name="Cup B", country_id=2, type="Cup", season="2024"),
    ]
    mock_championship_repository.get_all.return_value = mock_championships

    championships = championship_service.get_all_championships()

    assert championships == mock_championships
    mock_championship_repository.get_all.assert_called_once()

def test_get_all_championships_empty(championship_service, mock_championship_repository):
    mock_championship_repository.get_all.return_value = []

    championships = championship_service.get_all_championships()

    assert championships == []
    mock_championship_repository.get_all.assert_called_once()


def test_update_championship_success(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = Championship(id=1, name="Old Name", country_id=1, type="League", season="2023")
    mock_championship_repository.get_by_name.return_value = None # Adicionado: Simula que o novo nome não existe
    updated_championship = Championship(id=1, name="New Name", country_id=1, type="League", season="2023")
    mock_championship_repository.update.return_value = updated_championship

    championship = championship_service.update_championship(1, name="New Name")

    assert championship == updated_championship
    mock_championship_repository.get_by_id.assert_called_once_with(1)
    mock_championship_repository.get_by_name.assert_called_once_with("New Name") # Adicionado para verificar a chamada
    mock_championship_repository.update.assert_called_once_with(1, "New Name", None, None, None)


def test_update_championship_not_found_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = None
    mock_championship_repository.update.return_value = None

    with pytest.raises(ValueError, match="Campeonato não encontrado."):
        championship_service.update_championship(99, name="NonExistent")
    mock_championship_repository.get_by_id.assert_called_once_with(99)
    mock_championship_repository.update.assert_not_called()

def test_update_championship_partial_update(championship_service, mock_championship_repository):
    original_championship = Championship(id=1, name="League A", country_id=1, type="League", season="2023")
    mock_championship_repository.get_by_id.return_value = original_championship
    mock_championship_repository.get_by_name.return_value = None # Adicionado: Simula que o nome não será alterado para um existente
    updated_championship = Championship(id=1, name="League A", country_id=1, type="League", season="2024")
    mock_championship_repository.update.return_value = updated_championship

    championship = championship_service.update_championship(1, season="2024")

    assert championship == updated_championship
    mock_championship_repository.get_by_id.assert_called_once_with(1)
    mock_championship_repository.get_by_name.assert_not_called() # Não deve ser chamado se o nome não mudar
    mock_championship_repository.update.assert_called_once_with(1, None, None, None, "2024")

def test_update_championship_name_empty_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    with pytest.raises(ValueError, match="Championship name cannot be empty."):
        championship_service.update_championship(1, name="")
    mock_championship_repository.get_by_id.assert_called_once_with(1) # Deve ser chamado para verificar existência
    mock_championship_repository.update.assert_not_called() # Não deve chamar update se a validação falhar

def test_update_championship_name_not_string_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    with pytest.raises(ValueError, match="Championship name must be a string."):
        championship_service.update_championship(1, name=123)
    mock_championship_repository.get_by_id.assert_called_once_with(1)
    mock_championship_repository.update.assert_not_called()

def test_update_championship_name_too_long_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    with pytest.raises(ValueError, match="Championship name cannot exceed 100 characters."):
        championship_service.update_championship(1, name="a" * 101)
    mock_championship_repository.get_by_id.assert_called_once_with(1)
    mock_championship_repository.update.assert_not_called()

def test_delete_championship_success(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = Championship(id=1, name="Brasileirão", country_id=1, type="League", season="2023")
    mock_championship_repository.delete.return_value = True

    result = championship_service.delete_championship(1)

    assert result is True
    mock_championship_repository.get_by_id.assert_called_once_with(1)
    mock_championship_repository.delete.assert_called_once_with(1)

def test_delete_championship_not_found_raises_value_error(championship_service, mock_championship_repository):
    mock_championship_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Campeonato não encontrado."):
        championship_service.delete_championship(99)
    mock_championship_repository.get_by_id.assert_called_once_with(99)
    mock_championship_repository.delete.assert_not_called()