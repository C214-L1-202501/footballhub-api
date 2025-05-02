from typing import List
from app.schemas.country import Country
from app.repositories.countryRepository import CountryRepository


class CountryService:
    def __init__(self):
        self.repository = CountryRepository()

    def find_country_by_id(self, country_id: int) -> Country:
        """Find a country by its ID."""
        try:
            country = self.repository.get_by_id(country_id)
        except Exception as e:
            raise e
        return country

    def create_country(self, name: str) -> Country:
        """Create a new country."""
        country = self.repository.create(name)
        return country

    def get_all_countries(self) -> List[Country]:
        """Retrieve all countries from the database."""
        return self.repository.get_all()

    def update_country(self, country_id: int, name: str) -> Country:
        """Update a country's name."""
        country = self.repository.update(country_id, name)
        if not country:
            raise Exception("País não encontrado.")
        country.name = name
        return country

    def delete_country(self, country_id: int) -> bool:
        """Delete a country by its ID."""
        country = self.repository.get_by_id(country_id)
        if not country:
            raise Exception("País não encontrado.")
        return self.repository.delete(country_id)
