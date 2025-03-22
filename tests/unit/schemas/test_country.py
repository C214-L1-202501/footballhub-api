import pytest
from app.repositories.countryRepository import CountryRepository
from app.schemas.country import Country


class TestCountry:

    def test_create_country__happy_path__expected_country_created(self):
        # Fixture
        repository = CountryRepository()
        country_name = "Brasil"

        # Exercise
        country = repository.create(country_name)

        # Assert
        assert country is not None
        assert country.name == country_name

    def test_create_country__duplicate_name__expected_error(self):
        # Fixture
        repository = CountryRepository()
        country_name = "Brasil"
        
        # Pre-create the country
        repository.create(country_name)

        # Exercise & Assert
        with pytest.raises(Exception) as exc_info:
            repository.create(country_name)
        
        assert str(exc_info.value) == "Country with this name already exists"

    def test_get_country_by_name__existing_country__expected_country(self):
        # Fixture
        repository = CountryRepository()
        country_name = "Brasil"
        
        # Pre-create the country
        country = repository.create(country_name)

        # Exercise
        retrieved_country = repository.get_by_name(country_name)

        # Assert
        assert retrieved_country is not None
        assert retrieved_country.name == country_name

    def test_get_country_by_name__non_existing_country__expected_none(self):
        # Fixture
        repository = CountryRepository()
        country_name = "NonExistentCountry"

        # Exercise
        retrieved_country = repository.get_by_name(country_name)

        # Assert
        assert retrieved_country is None
