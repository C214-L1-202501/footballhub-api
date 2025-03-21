from typing import List
from app.schemas.country import Country
from app.repositories.countryRepository import CountryRepository


class CountryService:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    def find_country_by_id(self, country_id: int) -> Country:
        """Find a country by its ID."""
        country = self.repository.get_by_id(country_id)
        if not country:
            raise Exception("País não encontrado.")
        return country

    def create_country(self, name: str) -> Country:
        """Create a new country."""
        self.validate_country_creation(name)
        new_country = Country(name=name)
        self.repository.create(new_country)
        return new_country

    def get_all_countries(self) -> List[Country]:
        """Retrieve all countries from the database."""
        return self.repository.get_all()

    def update_country(self, country_id: int, name: str) -> Country:
        """Update a country's name."""
        self.validate_country_creation(name)
        country = self.repository.get_by_id(country_id)
        if not country:
            raise Exception("País não encontrado.")
        country.name = name
        self.repository.save(country)
        return country

    def delete_country(self, country_id: int) -> bool:
        """Delete a country by its ID."""
        country = self.repository.get_by_id(country_id)
        if not country:
            raise Exception("País não encontrado.")
        return self.repository.delete(country_id)
