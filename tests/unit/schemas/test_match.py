import pytest
from app.schemas.match import Match, Substitution

class TestMatch:

    def test_validate_different_teams__happy_path__expected_True():
        # Fixture
        home_team_id = 185
        away_team_id = 12

        # Exercise
        result = Match.Config.validate_different_teams(home_team_id, away_team_id)

        # Assert
        assert result is True

    def test_validate_different_teams__same_team__expected_error():
        # Fixture
        home_team_id = 18
        away_team_id = 18

        # Exercise & Assert
        with pytest.raises(ValueError) as exc_info:
            Match.Config.validate_different_teams(home_team_id, away_team_id)
        assert str(exc_info.value) == "home_team_id and away_team_id must be different"

    def test_validate_different_players__happy_path__expected_True():
        # Fixture
        player_out_id = 1100
        player_in_id = 152

        # Exercise
        result = Substitution.Config.validate_different_players(player_out_id, player_in_id)

        # Assert
        assert result is True

