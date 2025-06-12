from typing import List, Optional
from app.repositories.countryRepository import CountryRepository
from app.schemas.country import Country
from app.schemas.team import Team
from app.schemas.player import Player
from app.schemas.stadium import Stadium

class CountryService:
    def __init__(self, country_repository: CountryRepository = None):
        self.repository = country_repository if country_repository else CountryRepository()

    def find_country_by_id(self, country_id: int) -> Optional[Country]:
        return self.repository.get_by_id(country_id)

    def create_country(self, name: str) -> Country:
        if not name:
            raise ValueError("Country name cannot be empty.")
        if not isinstance(name, str):
            raise ValueError("Country name must be a string.")
        if len(name) > 100:
            raise ValueError("Country name cannot exceed 100 characters.")
        
        existing_country = self.repository.get_by_name(name)
        if existing_country:
            raise ValueError("Country with this name already exists.")
            
        return self.repository.create(name)

    def get_all_countries(self) -> List[Country]:
        return self.repository.get_all()

    def update_country(self, country_id: int, name: str) -> Optional[Country]:
        country = self.repository.get_by_id(country_id)
        if not country:
            raise ValueError("País não encontrado.")
        
        if not name:
            raise ValueError("Country name cannot be empty.")
        if not isinstance(name, str):
            raise ValueError("Country name must be a string.")
        if len(name) > 100:
            raise ValueError("Country name cannot exceed 100 characters.")

        return self.repository.update(country_id, name)

    def delete_country(self, country_id: int) -> bool:
        country = self.repository.get_by_id(country_id)
        if not country:
            raise ValueError("País não encontrado.")
        return self.repository.delete(country_id)

    def get_teams_by_country(self, country_id: int) -> List[Team]:
        country = self.repository.get_by_id(country_id)
        if not country:
            raise ValueError("País não encontrado.")
        return self.repository.get_teams(country_id)

    def get_players_by_country(self, country_id: int) -> List[Player]:
        country = self.repository.get_by_id(country_id)
        if not country:
            raise ValueError("País não encontrado.")
        return self.repository.get_players(country_id)

    def get_stadiums_by_country(self, country_id: int) -> List[Stadium]:
        country = self.repository.get_by_id(country_id)
        if not country:
            raise ValueError("País não encontrado.")
        return self.repository.get_stadiums(country_id)