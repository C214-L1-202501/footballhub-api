from typing import List, Optional
from app.schemas.championship import Championship
from app.repositories.championshipRepository import ChampionshipRepository
from app.services.countryService import CountryService


class ChampionshipService:
    def __init__(self, repository: ChampionshipRepository, country_service: CountryService):
        self.repository = repository
        self.country_service = country_service

    def create_championship(self, name: str, country_id: Optional[int] = None, 
                          type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        # Validate country exists if provided
        if country_id is not None:
            self.country_service.find_country_by_id(country_id)
        
        # Check if championship name already exists
        existing_championship = self.repository.get_by_name(name)
        if existing_championship:
            raise ValueError(f"Championship with name already exists.")
        
        # Validate type if provided
        if type and type not in ['League', 'Cup', 'Tournament', 'Friendly']:
            raise ValueError("Invalid championship type. Must be one of: 'League', 'Cup', 'Tournament', 'Friendly'")
        
        return self.repository.create(
            name=name,
            country_id=country_id,
            type=type,
            season=season
        )

    def get_championship_by_id(self, championship_id: int) -> Championship:
        """Get a championship by its ID."""
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise ValueError(f"Championship with ID {championship_id} not found.")
        return championship

    def get_championship_by_name(self, name: str) -> Championship:
        """Get a championship by its name."""
        championship = self.repository.get_by_name(name)
        if not championship:
            raise ValueError(f"Championship with name '{name}' not found.")
        return championship

    def get_all_championships(self) -> List[Championship]:
        """Get all championships."""
        return self.repository.get_all()

    def update_championship(self, championship_id: int, name: Optional[str] = None, 
                          country_id: Optional[int] = None, type: Optional[str] = None, 
                          season: Optional[str] = None) -> Championship:
        """Update championship information."""
        # Get existing championship
        championship = self.get_championship_by_id(championship_id)
        
        # Validate country if being updated
        if country_id is not None:
            self.country_service.find_country_by_id(country_id)
        
        # Check if new name already exists (if being changed)
        if name and name != championship.name:
            existing_championship = self.repository.get_by_name(name)
            if existing_championship:
                raise ValueError(f"Championship with name already exists.")
        
        # Validate type if provided
        if type and type not in ['League', 'Cup', 'Tournament', 'Friendly']:
            raise ValueError("Invalid championship type. Must be one of: 'League', 'Cup', 'Tournament', 'Friendly'")
        
        updated_championship = self.repository.update(
            championship_id=championship_id,
            name=name,
            country_id=country_id,
            type=type,
            season=season
        )
        
        if not updated_championship:
            raise ValueError("Failed to update championship.")
            
        return updated_championship

    def delete_championship(self, championship_id: int) -> bool:
        """Delete a championship by its ID."""
        # Verify championship exists first
        self.get_championship_by_id(championship_id)
        return self.repository.delete(championship_id)

    def get_championships_by_country(self, country_id: int) -> List[Championship]:
        """Get all championships from a specific country."""
        # Validate country exists
        self.country_service.find_country_by_id(country_id)
        
        with self.repository._get_session() as session:
            statement = select(Championship).where(Championship.country_id == country_id)
            championships = session.exec(statement).all()
            return championships

    def get_championships_by_type(self, type: str) -> List[Championship]:
        """Get all championships of a specific type."""
        valid_types = ['League', 'Cup', 'Tournament', 'Friendly']
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of: {valid_types}")
        
        with self.repository._get_session() as session:
            statement = select(Championship).where(Championship.type == type)
            championships = session.exec(statement).all()
            return championships