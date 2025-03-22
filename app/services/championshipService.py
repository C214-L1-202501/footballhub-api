from typing import List, Optional
from app.schemas.championship import Championship
from app.repositories.championshipRepository import ChampionshipRepository


class ChampionshipService:
    def __init__(self, repository: ChampionshipRepository):
        self.repository = repository

    def find_championship_by_id(self, championship_id: int) -> Championship:
        """Find a championship by its ID."""
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise Exception("Campeonato não encontrado.")
        return championship

    def create_championship(self, name: str, country_id: Optional[int] = None, type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        """Create a new championship."""
        self.validate_championship_creation(name, season)
        return self.repository.create(name, country_id, type, season)

    def get_all_championships(self) -> List[Championship]:
        """Retrieve all championships from the database."""
        return self.repository.get_all()

    def update_championship(self, championship_id: int, name: Optional[str] = None, country_id: Optional[int] = None, type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        """Update an existing championship's information."""
        self.validate_championship_update(name, season)
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise Exception("Campeonato não encontrado.")
        return self.repository.update(championship_id, name, country_id, type, season)

    def delete_championship(self, championship_id: int) -> bool:
        """Delete a championship by its ID."""
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise Exception("Campeonato não encontrado.")
        return self.repository.delete(championship_id)

    def validate_championship_creation(self, name: str, season: Optional[str]):
        """Validate the championship creation data."""
        if len(name) < 3:
            raise Exception("O nome do campeonato deve ter pelo menos 3 caracteres.")
        if season and not season.isdigit():
            raise Exception("A temporada deve ser um valor numérico válido.")

    def validate_championship_update(self, name: Optional[str], season: Optional[str]):
        """Validate the championship update data."""
        if name and len(name) < 3:
            raise Exception("O nome do campeonato deve ter pelo menos 3 caracteres.")
        if season and not season.isdigit():
            raise Exception("A temporada deve ser um valor numérico válido.")
