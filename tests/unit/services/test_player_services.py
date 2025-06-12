import pytest
from unittest.mock import MagicMock
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

print(f"DEBUG: Current working directory: {os.getcwd()}")
print(f"DEBUG: DATABASE_URL from os.getenv: {os.getenv('DATABASE_URL')}")

from app.services.PlayerService import PlayerService
from app.schemas.player import Player


@pytest.fixture
def mock_player_repository():
    return MagicMock()

@pytest.fixture
def player_service(mock_player_repository):
    service = PlayerService(player_repository=mock_player_repository)
    return service

# --- Testes para create_player ---
def test_create_player_success(player_service, mock_player_repository):
    mock_player_repository.create.return_value = Player(
        id=1, name="Lionel Messi", birth_date=datetime(1987, 6, 24),
        nationality_id=1, position="Forward", team_id=1
    )
    
    player = player_service.create_player(
        name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id=1, position="Forward", team_id=1
    )
    
    assert player.name == "Lionel Messi"
    assert player.id == 1
    mock_player_repository.create.assert_called_once_with(
        name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id=1, position="Forward", team_id=1
    )

def test_create_player_name_too_short_raises_value_error(player_service):
    with pytest.raises(ValueError, match="Nome deve ter entre 3 e 100 caracteres."):
        player_service.create_player(name="Li", birth_date=datetime(1987, 6, 24), nationality_id=1, position="Forward")

def test_create_player_invalid_nationality_id_raises_value_error(player_service):
    with pytest.raises(ValueError, match="ID da nacionalidade deve ser um número inteiro positivo"):
        player_service.create_player(name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id=0, position="Forward")
    with pytest.raises(ValueError, match="ID da nacionalidade deve ser um número inteiro positivo"):
        player_service.create_player(name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id="abc", position="Forward")

def test_create_player_invalid_team_id_raises_value_error(player_service):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo se fornecido"):
        player_service.create_player(name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id=1, position="Forward", team_id=-5)

def test_create_player_position_too_long_raises_value_error_from_schema(player_service):
    with pytest.raises(ValueError, match="Posição não pode exceder 50 caracteres."):
        player_service.create_player(name="Lionel Messi", birth_date=datetime(1987, 6, 24), nationality_id=1, position="a"*51)


def test_create_player_repository_integrity_error_name_birth_date_raises_value_error(player_service, mock_player_repository):
    from sqlalchemy.exc import IntegrityError
    mock_player_repository.create.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_player_name_birth_date\"", [], None)
    with pytest.raises(ValueError, match="Já existe um jogador com este nome e data de nascimento."):
        player_service.create_player(name="Existing Player", birth_date=datetime(2000, 1, 1), nationality_id=1, position="Midfielder")

def test_create_player_repository_sqlalchemy_error_raises_exception(player_service, mock_player_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_player_repository.create.side_effect = SQLAlchemyError("DB error")
    with pytest.raises(Exception, match="Erro no banco de dados ao criar jogador:"):
        player_service.create_player(name="Test Player", birth_date=datetime(2000, 1, 1), nationality_id=1, position="Forward")

# --- Testes para create_players ---
def test_create_players_success(player_service, mock_player_repository):
    players_data = [
        {"name": "Player A", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "Player B", "birth_date": datetime(2001,2,2), "nationality_id": 2, "position": "Defender"},
    ]
    mock_player_repository.create.side_effect = [
        Player(id=1, name="Player A", birth_date=datetime(2000,1,1), nationality_id=1, position="Attacker"),
        Player(id=2, name="Player B", birth_date=datetime(2001,2,2), nationality_id=2, position="Defender"),
    ]

    created_players = player_service.create_players(players_data)
    
    assert len(created_players) == 2
    assert created_players[0].name == "Player A"
    assert created_players[1].name == "Player B"
    assert mock_player_repository.create.call_count == 2
    mock_player_repository.create.assert_any_call(name="Player A", birth_date=datetime(2000,1,1), nationality_id=1, position="Attacker", team_id=None)
    mock_player_repository.create.assert_any_call(name="Player B", birth_date=datetime(2001,2,2), nationality_id=2, position="Defender", team_id=None)

def test_create_players_invalid_name_raises_value_error(player_service):
    players_data = [
        {"name": "Valid", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "In", "birth_date": datetime(2001,2,2), "nationality_id": 2, "position": "Defender"}, # Nome agora com menos de 3 caracteres
    ]
    with pytest.raises(ValueError, match="Nome inválido no jogador índice 1: 'In' \\(3-100 caracteres\\)"): # Ajustado nome
        player_service.create_players(players_data)

def test_create_players_invalid_nationality_id_raises_value_error(player_service):
    players_data = [
        {"name": "Player A", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "Player B", "birth_date": datetime(2001,2,2), "nationality_id": 0, "position": "Defender"}, # Invalid ID
    ]
    with pytest.raises(ValueError, match="ID da nacionalidade inválido no jogador índice 1: '0'"):
        player_service.create_players(players_data)

def test_create_players_invalid_position_too_long_raises_value_error(player_service):
    players_data = [
        {"name": "Player A", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "Player B", "birth_date": datetime(2001,2,2), "nationality_id": 2, "position": "a"*51}, # Invalid position
    ]
    # Usando r"" para raw string e ajustando regex para a string exata, escapando parênteses
    with pytest.raises(ValueError, match=r"Posição inválida no jogador índice 1: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \(máx 50 caracteres\)"): # Ajustado regex
        player_service.create_players(players_data)

def test_create_players_invalid_position_not_string_raises_value_error(player_service):
    players_data = [
        {"name": "Player A", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "Player B", "birth_date": datetime(2001,2,2), "nationality_id": 2, "position": 123}, # Invalid type
    ]
    with pytest.raises(ValueError, match=r"Posição inválida no jogador índice 1: '123' \(deve ser string ou None\)"): # Ajustado regex
        player_service.create_players(players_data)


def test_create_players_repository_integrity_error_raises_value_error(player_service, mock_player_repository):
    from sqlalchemy.exc import IntegrityError
    players_data = [
        {"name": "Player A", "birth_date": datetime(2000,1,1), "nationality_id": 1, "position": "Attacker"},
        {"name": "Player B", "birth_date": datetime(2001,2,2), "nationality_id": 2, "position": "Defender"},
    ]
    mock_player_repository.create.side_effect = [
        Player(id=1, name="Player A", birth_date=datetime(2000,1,1), nationality_id=1, position="Attacker"),
        IntegrityError("duplicate key value violates unique constraint \"uq_player_name_birth_date\"", [], None) # Second player fails
    ]
    with pytest.raises(ValueError, match="Já existe um jogador com este nome e data de nascimento no índice 1."):
        player_service.create_players(players_data)
    assert mock_player_repository.create.call_count == 2 # Called for both players

# --- Testes para get_player ---
def test_get_player_success(player_service, mock_player_repository):
    mock_player = Player(id=1, name="Neymar Jr", birth_date=datetime(1992, 2, 5), nationality_id=1, position="Forward")
    mock_player_repository.get_by_id.return_value = mock_player

    player = player_service.get_player(1)

    assert player == mock_player
    mock_player_repository.get_by_id.assert_called_once_with(1)

def test_get_player_not_found_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Jogador não encontrado."):
        player_service.get_player(99)
    mock_player_repository.get_by_id.assert_called_once_with(99)

# --- Testes para get_all_players ---
def test_get_all_players_success(player_service, mock_player_repository):
    mock_players = [
        Player(id=1, name="Player 1", birth_date=datetime(1990,1,1), nationality_id=1, position="Midfielder"),
        Player(id=2, name="Player 2", birth_date=datetime(1991,2,2), nationality_id=2, position="Defender")
    ]
    mock_player_repository.get_all.return_value = mock_players

    players = player_service.get_all_players()

    assert players == mock_players
    mock_player_repository.get_all.assert_called_once()

def test_get_all_players_empty(player_service, mock_player_repository):
    mock_player_repository.get_all.return_value = []

    players = player_service.get_all_players()

    assert players == []
    mock_player_repository.get_all.assert_called_once()

# --- Testes para update_player ---
def test_update_player_success(player_service, mock_player_repository):
    original_player = Player(id=1, name="Old Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    updated_player = Player(id=1, name="New Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    
    mock_player_repository.get_by_id.return_value = original_player
    mock_player_repository.update.return_value = updated_player

    player = player_service.update_player(1, name="New Name")

    assert player == updated_player
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_called_once_with(
        player_id=1, name="New Name", birth_date=None, nationality_id=None, position=None, team_id=None
    )

def test_update_player_not_found_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Jogador não encontrado."):
        player_service.update_player(99, name="Non Existent")
    mock_player_repository.get_by_id.assert_called_once_with(99)
    mock_player_repository.update.assert_not_called()

def test_update_player_name_too_short_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="Nome deve ser uma string com 3 a 100 caracteres"):
        player_service.update_player(1, name="Na")
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_invalid_name_type_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="Nome deve ser uma string com 3 a 100 caracteres"):
        player_service.update_player(1, name=123)
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_invalid_nationality_id_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="ID da nacionalidade deve ser um número inteiro positivo"):
        player_service.update_player(1, nationality_id=0)
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_invalid_position_type_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="Posição deve ser uma string ou None."):
        player_service.update_player(1, position=123)
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_position_too_long_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="Posição não pode exceder 50 caracteres."):
        player_service.update_player(1, position="a"*51)
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_invalid_team_id_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo"):
        player_service.update_player(1, team_id="abc")
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_not_called()

def test_update_player_repository_integrity_error_name_birth_date_raises_value_error(player_service, mock_player_repository):
    from sqlalchemy.exc import IntegrityError
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    mock_player_repository.update.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_player_name_birth_date\"", [], None)
    with pytest.raises(ValueError, match="Já existe um jogador com este nome e data de nascimento."):
        player_service.update_player(1, name="Existing Player", birth_date=datetime(2000, 1, 1))
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_called_once()


def test_update_player_repository_sqlalchemy_error_raises_exception(player_service, mock_player_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Valid Name", birth_date=datetime(1990,1,1), nationality_id=1, position="Forward")
    mock_player_repository.update.side_effect = SQLAlchemyError("Update DB error")
    with pytest.raises(Exception, match="Erro no banco de dados ao atualizar jogador:"):
        player_service.update_player(1, name="New Name")
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.update.assert_called_once()


# --- Testes para delete_player ---
def test_delete_player_success(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = Player(id=1, name="Player to Delete", birth_date=datetime(2000,1,1), nationality_id=1, position="Forward")
    mock_player_repository.delete.return_value = True

    result = player_service.delete_player(1)

    assert result is True
    mock_player_repository.get_by_id.assert_called_once_with(1)
    mock_player_repository.delete.assert_called_once_with(1)

def test_delete_player_not_found_raises_value_error(player_service, mock_player_repository):
    mock_player_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Jogador não encontrado."):
        player_service.delete_player(99)
    mock_player_repository.get_by_id.assert_called_once_with(99)
    mock_player_repository.delete.assert_not_called()