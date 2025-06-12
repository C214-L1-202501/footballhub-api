import pytest
from unittest.mock import Mock, MagicMock
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

from app.services.CountryService import CountryService
from app.schemas.country import Country
from app.schemas.team import Team
from app.schemas.player import Player
from app.schemas.stadium import Stadium


@pytest.fixture
def mock_country_repository():
    return MagicMock()


@pytest.fixture
def country_service(mock_country_repository):
    service = CountryService(country_repository=mock_country_repository)
    return service


def test_find_country_by_id_success(country_service, mock_country_repository):
    mock_country = Country(id=1, name="Brazil")
    mock_country_repository.get_by_id.return_value = mock_country

    country = country_service.find_country_by_id(1)

    assert country == mock_country
    mock_country_repository.get_by_id.assert_called_once_with(1)


def test_find_country_by_id_not_found(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    country = country_service.find_country_by_id(99)

    assert country is None
    mock_country_repository.get_by_id.assert_called_once_with(99)


def test_find_country_by_id_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        country_service.find_country_by_id(1)
    mock_country_repository.get_by_id.assert_called_once_with(1)


def test_create_country_success(country_service, mock_country_repository):
    mock_country_repository.get_by_name.return_value = None
    mock_country = Country(id=1, name="NewCountry")
    mock_country_repository.create.return_value = mock_country

    country = country_service.create_country("NewCountry")

    assert country == mock_country
    mock_country_repository.get_by_name.assert_called_once_with("NewCountry")
    mock_country_repository.create.assert_called_once_with("NewCountry")


def test_create_country_name_empty_raises_exception(country_service):
    with pytest.raises(ValueError, match="Country name cannot be empty."):
        country_service.create_country("")


def test_create_country_name_not_string_raises_exception(country_service):
    with pytest.raises(ValueError, match="Country name must be a string."):
        country_service.create_country(123)


def test_create_country_name_too_long_raises_exception(country_service):
    with pytest.raises(ValueError, match="Country name cannot exceed 100 characters."):
        country_service.create_country("a" * 101)


def test_create_country_name_already_exists_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_name.return_value = Country(id=1, name="ExistingCountry")

    with pytest.raises(ValueError, match="Country with this name already exists."):
        country_service.create_country("ExistingCountry")
    mock_country_repository.get_by_name.assert_called_once_with("ExistingCountry")
    mock_country_repository.create.assert_not_called()


def test_get_all_countries_success(country_service, mock_country_repository):
    mock_countries = [Country(id=1, name="CountryA"), Country(id=2, name="CountryB")]
    mock_country_repository.get_all.return_value = mock_countries

    countries = country_service.get_all_countries()

    assert countries == mock_countries
    mock_country_repository.get_all.assert_called_once()


def test_get_all_countries_empty(country_service, mock_country_repository):
    mock_country_repository.get_all.return_value = []

    countries = country_service.get_all_countries()

    assert countries == []
    mock_country_repository.get_all.assert_called_once()


def test_update_country_success(country_service, mock_country_repository):
    mock_country = Country(id=1, name="OldCountry")
    mock_country_repository.get_by_id.return_value = mock_country
    updated_country = Country(id=1, name="UpdatedCountry")
    mock_country_repository.update.return_value = updated_country

    country = country_service.update_country(1, "UpdatedCountry")

    assert country == updated_country
    mock_country_repository.get_by_id.assert_called_once_with(1)
    mock_country_repository.update.assert_called_once_with(1, "UpdatedCountry")


def test_update_country_not_found_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="País não encontrado."):
        country_service.update_country(99, "NonExistent")
    mock_country_repository.get_by_id.assert_called_once_with(99)
    mock_country_repository.update.assert_not_called()


def test_update_country_name_empty_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    with pytest.raises(ValueError, match="Country name cannot be empty."):
        country_service.update_country(1, "")


def test_update_country_name_not_string_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    with pytest.raises(ValueError, match="Country name must be a string."):
        country_service.update_country(1, 123)


def test_update_country_name_too_long_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    with pytest.raises(ValueError, match="Country name cannot exceed 100 characters."):
        country_service.update_country(1, "a" * 101)


def test_delete_country_success(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    mock_country_repository.delete.return_value = True

    result = country_service.delete_country(1)

    assert result is True
    mock_country_repository.get_by_id.assert_called_once_with(1)
    mock_country_repository.delete.assert_called_once_with(1)


def test_delete_country_not_found_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="País não encontrado."):
        country_service.delete_country(99)
    mock_country_repository.get_by_id.assert_called_once_with(99)
    mock_country_repository.delete.assert_not_called()


def test_get_teams_by_country_success(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    mock_teams = [
        Team(id=1, name="Team A", country_id=1, city="City A", stadium_id=1),
        Team(id=2, name="Team B", country_id=1, city="City B", stadium_id=2),
    ]
    mock_country_repository.get_teams.return_value = mock_teams

    teams = country_service.get_teams_by_country(1)

    assert teams == mock_teams
    mock_country_repository.get_by_id.assert_called_once_with(1)
    mock_country_repository.get_teams.assert_called_once_with(1)


def test_get_teams_by_country_not_found_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="País não encontrado."):
        country_service.get_teams_by_country(99)
    mock_country_repository.get_by_id.assert_called_once_with(99)
    mock_country_repository.get_teams.assert_not_called()


def test_get_players_by_country_success(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    mock_players = [
        Player(id=1, name="Player X", country_id=1, nationality_id=1, team_id=1, birth_date="2000-01-01", position="Attacker"),
        Player(id=2, name="Player Y", country_id=1, nationality_id=1, team_id=1, birth_date="2001-01-01", position="Midfielder"),
    ]
    mock_country_repository.get_players.return_value = mock_players

    players = country_service.get_players_by_country(1)

    assert players == mock_players
    mock_country_repository.get_by_id.assert_called_once_with(1)
    mock_country_repository.get_players.assert_called_once_with(1)


def test_get_players_by_country_not_found_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="País não encontrado."):
        country_service.get_players_by_country(99)
    mock_country_repository.get_by_id.assert_called_once_with(99)
    mock_country_repository.get_players.assert_not_called()


def test_get_stadiums_by_country_success(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = Country(id=1, name="Brazil")
    mock_stadiums = [
        Stadium(id=1, name="Stadium A", capacity=50000, country_id=1, city="City A"),
        Stadium(id=2, name="Stadium B", capacity=60000, country_id=1, city="City B"),
    ]
    mock_country_repository.get_stadiums.return_value = mock_stadiums

    stadiums = country_service.get_stadiums_by_country(1)

    assert stadiums == mock_stadiums
    mock_country_repository.get_by_id.assert_called_once_with(1)
    mock_country_repository.get_stadiums.assert_called_once_with(1)


def test_get_stadiums_by_country_not_found_raises_exception(country_service, mock_country_repository):
    mock_country_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="País não encontrado."):
        country_service.get_stadiums_by_country(99)
    mock_country_repository.get_by_id.assert_called_once_with(99)
    mock_country_repository.get_stadiums.assert_not_called()