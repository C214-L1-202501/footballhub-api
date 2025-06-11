import pytest
from app.schemas.match import Match, Substitution

class TestMatch:
    def test_validate_different_teams__happy_path__expected_True(self):
        home_team_id = 185
        away_team_id = 12
        result = Match.validate_different_teams(home_team_id, away_team_id)
        assert result is True

    def test_validate_different_teams__same_team__expected_error(self):
        home_team_id = 18
        away_team_id = 18
        with pytest.raises(ValueError) as exc_info:
            Match.validate_different_teams(home_team_id, away_team_id)
        assert str(exc_info.value) == "home_team_id e away_team_id devem ser diferentes"

class TestSubstitution:
    def test_validate_different_players__happy_path__expected_True(self):
        player_out_id = 1100
        player_in_id = 152
        result = Substitution.validate_different_players(player_out_id, player_in_id)
        assert result is True

    def test_validate_different_players__same_player__expected_error(self):
        player_out_id = 100
        player_in_id = 100
        with pytest.raises(ValueError) as exc_info:
            Substitution.validate_different_players(player_out_id, player_in_id)
        assert str(exc_info.value) == "player_out_id e player_in_id devem ser diferentes"