import pytest
from app.schemas.player import Player
from datetime import datetime

class TestPlayer:

    def test_create_player_with_all_fields_success(self):
        player = Player(
            id=1,
            name="Lionel Messi",
            nationality_id=1,
            team_id=10,
            birth_date=datetime(1987, 6, 24),
            position="Forward"
        )
        assert player.id == 1
        assert player.name == "Lionel Messi"
        assert player.nationality_id == 1
        assert player.team_id == 10
        assert player.birth_date == datetime(1987, 6, 24)
        assert player.position == "Forward"

    def test_create_player_with_required_fields_only(self):
        player = Player(
            name="Cristiano Ronaldo",
            nationality_id=2
        )
        assert player.name == "Cristiano Ronaldo"
        assert player.nationality_id == 2
        assert player.team_id is None
        assert player.birth_date is None
        assert player.position is None

    def test_player_name_max_length(self):
        name = "X" * 100
        player = Player(name=name, nationality_id=1)
        assert player.name == name

    def test_player_name_exceeds_max_length(self):
        name = "X" * 101
        with pytest.raises(ValueError) as exc_info:
            Player(name=name, nationality_id=1)
        assert "Player name cannot exceed 100 characters" in str(exc_info.value)

    def test_player_position_max_length(self):
        position = "Goalkeeper" * 5 # Total de 50 caracteres
        player = Player(name="Alisson Becker", nationality_id=3, position=position)
        assert player.position == position

    def test_player_position_exceeds_max_length(self):
        position = "Goalkeeper" * 6 # Total de 60 caracteres
        with pytest.raises(ValueError) as exc_info:
            Player(name="Thibaut Courtois", nationality_id=4, position=position)
        assert "Player position cannot exceed 50 characters" in str(exc_info.value)

    def test_player_name_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Player(name=None, nationality_id=1)
        assert "Player name is required" in str(exc_info.value)

    def test_player_nationality_id_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Player(name="Neymar Jr.", nationality_id=None)
        assert "Player nationality ID is required" in str(exc_info.value)
