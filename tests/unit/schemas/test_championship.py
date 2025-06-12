import pytest
from app.schemas.championship import Championship

class TestChampionship:
    def test_create_championship_with_all_fields_success(self):
        championship = Championship(
            id=1,
            name="Premier League",
            country_id=10,
            type="League",
            start_date="2024-08-01",
            end_date="2025-05-31"
        )
        assert championship.name == "Premier League"
        assert championship.country_id == 10
        assert championship.type == "League"

    def test_create_championship_missing_optional_fields(self):
        championship = Championship(
            name="La Liga",
            country_id=1
        )
        assert championship.name == "La Liga"
        assert championship.country_id == 1
        assert championship.type is None

    def test_championship_name_max_length(self):
        name = "A" * 100
        championship = Championship(name=name, country_id=1)
        assert championship.name == name

    def test_championship_name_exceeds_max_length(self):
        name = "A" * 101 
        with pytest.raises(ValueError) as exc_info:
            Championship(name=name, country_id=1)
        assert "Championship name cannot exceed 100 characters" in str(exc_info.value)