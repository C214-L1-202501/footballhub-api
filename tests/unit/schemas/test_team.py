import pytest
from app.schemas.team import Team, ChampionshipParticipation
from datetime import datetime

class TestTeam:

    def test_create_team_with_all_fields_success(self):
        team = Team(
            id=1,
            name="Real Madrid",
            nickname="Los Blancos",
            city="Madrid",
            country_id=1,
            founding_date=datetime(1902, 3, 6)
        )
        assert team.id == 1
        assert team.name == "Real Madrid"
        assert team.nickname == "Los Blancos"
        assert team.city == "Madrid"
        assert team.country_id == 1
        assert team.founding_date == datetime(1902, 3, 6)

    def test_create_team_with_required_fields_only(self):
        team = Team(
            name="FC Barcelona",
            country_id=1
        )
        assert team.name == "FC Barcelona"
        assert team.country_id == 1
        assert team.nickname is None
        assert team.city is None
        assert team.founding_date is None

    def test_team_name_max_length(self):
        name = "A" * 100
        team = Team(name=name, country_id=1)
        assert team.name == name

    def test_team_name_exceeds_max_length(self):
        name = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            Team(name=name, country_id=1)
        assert "Team name cannot exceed 100 characters" in str(exc_info.value)

    def test_team_nickname_max_length(self):
        nickname = "B" * 50
        team = Team(name="Test Team", country_id=1, nickname=nickname)
        assert team.nickname == nickname

    def test_team_nickname_exceeds_max_length(self):
        nickname = "B" * 51
        with pytest.raises(ValueError) as exc_info:
            Team(name="Test Team", country_id=1, nickname=nickname)
        assert "Team nickname cannot exceed 50 characters" in str(exc_info.value)

    def test_team_city_max_length(self):
        city = "C" * 100
        team = Team(name="Test City Team", country_id=1, city=city)
        assert team.city == city

    def test_team_city_exceeds_max_length(self):
        city = "C" * 101
        with pytest.raises(ValueError) as exc_info:
            Team(name="Test City Team", country_id=1, city=city)
        assert "Team city cannot exceed 100 characters" in str(exc_info.value)

    def test_team_name_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Team(name=None, country_id=1)
        assert "Team name is required" in str(exc_info.value)

    def test_team_country_id_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            Team(name="Missing Country Team", country_id=None)
        assert "Country ID is required" in str(exc_info.value)

class TestChampionshipParticipation:

    def test_create_championship_participation_with_all_fields_success(self):
        participation = ChampionshipParticipation(
            id=1,
            championship_id=10,
            team_id=20,
            season="2024-2025"
        )
        assert participation.id == 1
        assert participation.championship_id == 10
        assert participation.team_id == 20
        assert participation.season == "2024-2025"

    def test_create_championship_participation_with_required_fields_only(self):
        participation = ChampionshipParticipation(
            championship_id=11,
            team_id=21
        )
        assert participation.championship_id == 11
        assert participation.team_id == 21
        assert participation.season is None

    def test_championship_participation_season_max_length(self):
        season = "D" * 20
        participation = ChampionshipParticipation(championship_id=12, team_id=22, season=season)
        assert participation.season == season

    def test_championship_participation_season_exceeds_max_length(self):
        season = "D" * 21
        with pytest.raises(ValueError) as exc_info:
            ChampionshipParticipation(championship_id=13, team_id=23, season=season)
        assert "Season cannot exceed 20 characters" in str(exc_info.value)

    def test_championship_participation_championship_id_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            ChampionshipParticipation(championship_id=None, team_id=1)
        assert "Championship ID is required for Championship Participation" in str(exc_info.value)

    def test_championship_participation_team_id_not_nullable(self):
        with pytest.raises(ValueError) as exc_info:
            ChampionshipParticipation(championship_id=1, team_id=None)
        assert "Team ID is required for Championship Participation" in str(exc_info.value)