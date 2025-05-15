from typing import List, Optional
from app.schemas.championship import Championship
from app.repositories.championshipRepository import ChampionshipRepository


class ChampionshipService:
    def __init__(self):
        self.repository = ChampionshipRepository()

    def find_championship_by_id(self, championship_id: int) -> Championship:
        """Find a championship by its ID."""
        try:
            championship = self.repository.get_by_id(championship_id)
        except Exception as e:
            raise e
        return championship
    
    def find_championship_by_name(self, name: str) -> Championship:
        """Find a championship by its ID."""
        try:
            championship = self.repository.get_by_name(name)
        except Exception as e:
            raise e
        return championship

    def create_championship(self, name: str, country_id: Optional[int], type: Optional[str], season: Optional[str]) -> Championship:
        """Create a new championship."""
        championship = self.repository.create(name, country_id, type, season)
        return championship

    def get_all_championships(self) -> List[Championship]:
        """Retrieve all championships."""
        return self.repository.get_all()

    def update_championship(self, championship_id: int, name: Optional[str] = None, country_id: Optional[int] = None,
                            type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        """Update a championship by its ID."""
        championship = self.repository.update(championship_id, name, country_id, type, season)
        if not championship:
            raise Exception("Campeonato não encontrado.")
        return championship

    def delete_championship(self, championship_id: int) -> bool:
        """Delete a championship by its ID."""
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise Exception("Campeonato não encontrado.")
        return self.repository.delete(championship_id)
