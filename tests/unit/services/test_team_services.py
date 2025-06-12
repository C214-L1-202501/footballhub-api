import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.services.TeamService import TeamService
from app.schemas.team import Team, ChampionshipParticipation
from app.schemas.player import Player

@pytest.fixture
def mock_team_repository():
    return MagicMock()

@pytest.fixture
def team_service(mock_team_repository):
    return TeamService(team_repository=mock_team_repository)

def test_create_team_success(team_service, mock_team_repository):
    mock_team_repository.create.return_value = Team(
        id=1, name="Flamengo", country_id=1, nickname="Mengão", city="Rio de Janeiro", founding_date=datetime(1895, 11, 15)
    )
    
    team = team_service.create_team(
        name="Flamengo", country_id=1, nickname="Mengão", city="Rio de Janeiro", founding_date=datetime(1895, 11, 15)
    )
    
    assert team.name == "Flamengo"
    assert team.country_id == 1
    mock_team_repository.create.assert_called_once_with(
        name="Flamengo", country_id=1, nickname="Mengão", city="Rio de Janeiro", founding_date=datetime(1895, 11, 15)
    )

@pytest.mark.parametrize("name", ["", "  ", None])
def test_create_team_invalid_name(team_service, name):
    with pytest.raises(ValueError, match="Nome do time é obrigatório."):
        team_service.create_team(name=name, country_id=1)

@pytest.mark.parametrize("name", ["ab", "a" * 101])
def test_create_team_name_length_validation(team_service, name):
    with pytest.raises(ValueError, match="Nome do time deve ter entre 3 e 100 caracteres."):
        team_service.create_team(name=name, country_id=1)

@pytest.mark.parametrize("country_id", [0, -1, "abc", None])
def test_create_team_invalid_country_id(team_service, country_id):
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        team_service.create_team(name="Test Team", country_id=country_id)

@pytest.mark.parametrize("nickname", ["a", "a" * 51])
def test_create_team_nickname_length_validation(team_service, nickname):
    with pytest.raises(ValueError, match="Apelido do time deve ter entre 2 e 50 caracteres"):
        team_service.create_team(name="Test Team", country_id=1, nickname=nickname)

@pytest.mark.parametrize("city", ["a", "a" * 101])
def test_create_team_city_length_validation(team_service, city):
    with pytest.raises(ValueError, match="Cidade do time deve ter entre 2 e 100 caracteres"):
        team_service.create_team(name="Test Team", country_id=1, city=city)

def test_create_team_future_founding_date(team_service):
    future_date = datetime(2050, 1, 1)
    with pytest.raises(ValueError, match="Data de fundação não pode ser no futuro."):
        team_service.create_team(name="Future Team", country_id=1, founding_date=future_date)

def test_create_team_integrity_error_duplicate_name(team_service, mock_team_repository):
    from sqlalchemy.exc import IntegrityError
    mock_team_repository.create.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_team_name\"", [], None)
    
    with pytest.raises(ValueError, match="Já existe um time com o nome 'Existing Team'."):
        team_service.create_team(name="Existing Team", country_id=1)

def test_create_team_repository_error(team_service, mock_team_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.create.side_effect = SQLAlchemyError("Database connection error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao criar time:"):
        team_service.create_team(name="Error Team", country_id=1)

def test_get_team_success(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Corinthians", country_id=1)
    
    team = team_service.get_team(1)
    
    assert team.name == "Corinthians"
    mock_team_repository.get_by_id.assert_called_once_with(1)

def test_get_team_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Time com ID 999 não encontrado."):
        team_service.get_team(999)
    
    mock_team_repository.get_by_id.assert_called_once_with(999)

@pytest.mark.parametrize("team_id", [0, -1, "abc"])
def test_get_team_invalid_id(team_service, team_id):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.get_team(team_id)

def test_get_team_repository_error(team_service, mock_team_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_by_id.side_effect = SQLAlchemyError("DB error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao buscar time por ID:"):
        team_service.get_team(1)

def test_search_teams_success(team_service, mock_team_repository):
    mock_team_repository.get_by_name.return_value = Team(id=1, name="Grêmio", country_id=1)
    
    teams = team_service.search_teams("Grêmio")
    
    assert len(teams) == 1
    assert teams[0].name == "Grêmio"
    mock_team_repository.get_by_name.assert_called_once_with("Grêmio")

def test_search_teams_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_name.return_value = None
    
    with pytest.raises(ValueError, match="Time com nome 'NonExistent' não encontrado."):
        team_service.search_teams("NonExistent")
    
    mock_team_repository.get_by_name.assert_called_once_with("NonExistent")

@pytest.mark.parametrize("name", ["", "  ", None])
def test_search_teams_invalid_name(team_service, name):
    with pytest.raises(ValueError, match="Nome para busca do time deve ser uma string não vazia."):
        team_service.search_teams(name)

def test_search_teams_repository_error(team_service, mock_team_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_by_name.side_effect = SQLAlchemyError("DB search error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao buscar time por nome:"):
        team_service.search_teams("Any Name")

def test_get_all_teams_success(team_service, mock_team_repository):
    mock_team_repository.get_all.return_value = [
        Team(id=1, name="Team A", country_id=1),
        Team(id=2, name="Team B", country_id=1)
    ]
    
    teams = team_service.get_all_teams()
    
    assert len(teams) == 2
    assert teams[0].name == "Team A"
    mock_team_repository.get_all.assert_called_once()

def test_get_all_teams_empty(team_service, mock_team_repository):
    mock_team_repository.get_all.return_value = []
    
    teams = team_service.get_all_teams()
    
    assert len(teams) == 0
    mock_team_repository.get_all.assert_called_once()

def test_get_all_teams_repository_error(team_service, mock_team_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_all.side_effect = SQLAlchemyError("DB fetch all error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao recuperar todos os times:"):
        team_service.get_all_teams()

@pytest.fixture
def existing_team():
    return Team(id=1, name="Old Name", country_id=1, nickname="Old Nick", city="Old City", founding_date=datetime(2000, 1, 1))

def test_update_team_success(team_service, mock_team_repository, existing_team):
    mock_team_repository.get_by_id.return_value = existing_team
    updated_team_mock = Team(id=1, name="New Name", country_id=1, nickname="New Nick", city="New City", founding_date=datetime(2000, 1, 1))
    mock_team_repository.update.return_value = updated_team_mock
    
    team = team_service.update_team(
        team_id=1, name="New Name", nickname="New Nick", city="New City"
    )
    
    assert team.name == "New Name"
    assert team.nickname == "New Nick"
    assert team.city == "New City"
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.update.assert_called_once_with(
        1, name="New Name", nickname="New Nick", city="New City"
    )

def test_update_team_no_changes(team_service, mock_team_repository, existing_team):
    mock_team_repository.get_by_id.return_value = existing_team
    
    team = team_service.update_team(1)
    
    assert team == existing_team
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.update.assert_not_called()

def test_update_team_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Time com ID 999 não encontrado para atualização."):
        team_service.update_team(999, name="New Name")
    
    mock_team_repository.get_by_id.assert_called_once_with(999)
    mock_team_repository.update.assert_not_called()

def test_update_team_invalid_id(team_service):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.update_team(0, name="Test")

def test_update_team_invalid_name(team_service, mock_team_repository, existing_team):
    mock_team_repository.get_by_id.return_value = existing_team
    with pytest.raises(ValueError, match="Nome do time não pode ser vazio ou inválido."):
        team_service.update_team(1, name="  ")
    with pytest.raises(ValueError, match="Nome do time deve ter entre 3 e 100 caracteres."):
        team_service.update_team(1, name="ab")
    mock_team_repository.update.assert_not_called()

def test_update_team_invalid_country_id(team_service, mock_team_repository, existing_team):
    mock_team_repository.get_by_id.return_value = existing_team
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        team_service.update_team(1, country_id=0)
    mock_team_repository.update.assert_not_called()

def test_update_team_future_founding_date(team_service, mock_team_repository, existing_team):
    mock_team_repository.get_by_id.return_value = existing_team
    future_date = datetime(2050, 1, 1)
    with pytest.raises(ValueError, match="Data de fundação não pode ser no futuro."):
        team_service.update_team(1, founding_date=future_date)
    mock_team_repository.update.assert_not_called()

def test_update_team_integrity_error_duplicate_name(team_service, mock_team_repository, existing_team):
    from sqlalchemy.exc import IntegrityError
    mock_team_repository.get_by_id.return_value = existing_team
    mock_team_repository.update.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_team_name\"", [], None)
    
    with pytest.raises(ValueError, match="Já existe um time com o nome 'Another Team'."):
        team_service.update_team(1, name="Another Team")
    mock_team_repository.update.assert_called_once()

def test_update_team_repository_error(team_service, mock_team_repository, existing_team):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_by_id.return_value = existing_team
    mock_team_repository.update.side_effect = SQLAlchemyError("DB update error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao atualizar time:"):
        team_service.update_team(1, name="Error Update")
    mock_team_repository.update.assert_called_once()

def test_delete_team_success(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="To Delete", country_id=1)
    mock_team_repository.delete.return_value = True
    
    result = team_service.delete_team(1)
    
    assert result is True
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.delete.assert_called_once_with(1)

def test_delete_team_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Time com ID 999 não encontrado para exclusão."):
        team_service.delete_team(999)
    
    mock_team_repository.get_by_id.assert_called_once_with(999)
    mock_team_repository.delete.assert_not_called()

@pytest.mark.parametrize("team_id", [0, -1, "abc"])
def test_delete_team_invalid_id(team_service, team_id):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.delete_team(team_id)

def test_delete_team_repository_error(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Error Team", country_id=1)
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.delete.side_effect = SQLAlchemyError("DB delete error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao excluir time:"):
        team_service.delete_team(1)
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.delete.assert_called_once_with(1)

def test_get_players_by_team_success(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Team With Players", country_id=1)
    mock_team_repository.get_players_for_team.return_value = [
        Player(id=1, name="Player 1", team_id=1, country_id=1, nationality_id=1),
        Player(id=2, name="Player 2", team_id=1, country_id=1, nationality_id=1)
    ]
    
    players = team_service.get_players_by_team(1)
    
    assert len(players) == 2
    assert players[0].name == "Player 1"
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.get_players_for_team.assert_called_once_with(1)

def test_get_players_by_team_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Time com ID 999 não encontrado para listar jogadores."):
        team_service.get_players_by_team(999)
    
    mock_team_repository.get_by_id.assert_called_once_with(999)
    mock_team_repository.get_players_for_team.assert_not_called()

@pytest.mark.parametrize("team_id", [0, -1, "abc"])
def test_get_players_by_team_invalid_id(team_service, team_id):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.get_players_by_team(team_id)

def test_get_players_by_team_repository_error(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Team", country_id=1)
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_players_for_team.side_effect = SQLAlchemyError("DB players error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao recuperar jogadores do time:"):
        team_service.get_players_by_team(1)
    mock_team_repository.get_players_for_team.assert_called_once_with(1)

def test_create_championship_participation_success(team_service, mock_team_repository):
    mock_team_repository.create_championship_participation.return_value = ChampionshipParticipation(
        id=1, championship_id=1, team_id=1, season="2024"
    )
    
    participation = team_service.create_championship_participation(
        championship_id=1, team_id=1, season="2024"
    )
    
    assert participation.season == "2024"
    mock_team_repository.create_championship_participation.assert_called_once_with(
        championship_id=1, team_id=1, season="2024"
    )

@pytest.mark.parametrize("champ_id", [0, -1, "abc"])
def test_create_championship_participation_invalid_champ_id(team_service, champ_id):
    with pytest.raises(ValueError, match="ID do campeonato deve ser um número inteiro positivo."):
        team_service.create_championship_participation(championship_id=champ_id, team_id=1)

@pytest.mark.parametrize("team_id", [0, -1, "abc"])
def test_create_championship_participation_invalid_team_id(team_service, team_id):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.create_championship_participation(championship_id=1, team_id=team_id)

def test_create_championship_participation_season_too_long(team_service):
    with pytest.raises(ValueError, match="A temporada deve ter no máximo 20 caracteres"):
        team_service.create_championship_participation(championship_id=1, team_id=1, season="a" * 21)

def test_create_championship_participation_integrity_error_duplicate(team_service, mock_team_repository):
    from sqlalchemy.exc import IntegrityError
    mock_team_repository.create_championship_participation.side_effect = IntegrityError(
        "duplicate key value violates unique constraint \"uq_championship_participation\"", [], None
    )
    
    with pytest.raises(ValueError, match="Esta participação em campeonato já existe para o time 1 e campeonato 1 na temporada 2024."):
        team_service.create_championship_participation(championship_id=1, team_id=1, season="2024")

def test_create_championship_participation_repository_error(team_service, mock_team_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.create_championship_participation.side_effect = SQLAlchemyError("DB participation error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao criar participação em campeonato:"):
        team_service.create_championship_participation(championship_id=1, team_id=1, season="2024")

def test_delete_championship_participation_success(team_service, mock_team_repository):
    mock_team_repository.get_championship_participation_by_id.return_value = ChampionshipParticipation(
        id=1, championship_id=1, team_id=1
    )
    mock_team_repository.delete_championship_participation.return_value = True
    
    result = team_service.delete_championship_participation(1)
    
    assert result is True
    mock_team_repository.get_championship_participation_by_id.assert_called_once_with(1)
    mock_team_repository.delete_championship_participation.assert_called_once_with(1)

def test_delete_championship_participation_not_found(team_service, mock_team_repository):
    mock_team_repository.get_championship_participation_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Participação em campeonato com ID 999 não encontrada para exclusão."):
        team_service.delete_championship_participation(999)
    
    mock_team_repository.get_championship_participation_by_id.assert_called_once_with(999)
    mock_team_repository.delete_championship_participation.assert_not_called()

@pytest.mark.parametrize("participation_id", [0, -1, "abc"])
def test_delete_championship_participation_invalid_id(team_service, participation_id):
    with pytest.raises(ValueError, match="ID de participação deve ser um número inteiro positivo."):
        team_service.delete_championship_participation(participation_id)

def test_delete_championship_participation_repository_error(team_service, mock_team_repository):
    mock_team_repository.get_championship_participation_by_id.return_value = ChampionshipParticipation(
        id=1, championship_id=1, team_id=1
    )
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.delete_championship_participation.side_effect = SQLAlchemyError("DB delete participation error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao excluir participação em campeonato:"):
        team_service.delete_championship_participation(1)
    mock_team_repository.get_championship_participation_by_id.assert_called_once_with(1)
    mock_team_repository.delete_championship_participation.assert_called_once_with(1)

def test_get_participations_by_team_success(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Team with Participations", country_id=1)
    mock_team_repository.get_team_championship_participations.return_value = [
        {"id": 1, "championship_id": 101, "championship_name": "League A", "team_id": 1, "season": "2023"},
        {"id": 2, "championship_id": 102, "championship_name": "Cup B", "team_id": 1, "season": "2024"},
    ]
    
    participations = team_service.get_participations_by_team(1)
    
    assert len(participations) == 2
    assert participations[0]["championship_name"] == "League A"
    mock_team_repository.get_by_id.assert_called_once_with(1)
    mock_team_repository.get_team_championship_participations.assert_called_once_with(1)

def test_get_participations_by_team_not_found(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Time com ID 999 não encontrado para listar participações em campeonatos."):
        team_service.get_participations_by_team(999)
    
    mock_team_repository.get_by_id.assert_called_once_with(999)
    mock_team_repository.get_team_championship_participations.assert_not_called()

@pytest.mark.parametrize("team_id", [0, -1, "abc"])
def test_get_participations_by_team_invalid_id(team_service, team_id):
    with pytest.raises(ValueError, match="ID do time deve ser um número inteiro positivo."):
        team_service.get_participations_by_team(team_id)

def test_get_participations_by_team_repository_error(team_service, mock_team_repository):
    mock_team_repository.get_by_id.return_value = Team(id=1, name="Team", country_id=1)
    from sqlalchemy.exc import SQLAlchemyError
    mock_team_repository.get_team_championship_participations.side_effect = SQLAlchemyError("DB participations error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao recuperar participações em campeonatos do time:"):
        team_service.get_participations_by_team(1)
    mock_team_repository.get_team_championship_participations.assert_called_once_with(1)