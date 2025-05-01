from typing import List, Optional
from app.schemas.stadium import Stadium
from app.repositories.stadiumRepository import StadiumRepository


class StadiumService:
    def __init__(self, repository: StadiumRepository):
        self.repository = repository

    def create_stadium(self, name: str, city: str, country_id: int) -> Stadium:
        """Create a new stadium after validating input."""
        if not name or not city:
            raise ValueError("Name and city are required for stadium creation.")
        if country_id <= 0:
            raise ValueError("Invalid country ID.")

        return self.repository.create(name=name, city=city, country_id=country_id)

    def get_stadium_by_id(self, stadium_id: int) -> Stadium:
        """Retrieve a stadium by ID with validation."""
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise ValueError(f"Stadium with ID {stadium_id} not found.")
        return stadium

    def get_all_stadiums(self) -> List[Stadium]:
        """List all stadiums."""
        return self.repository.get_all()

    def update_stadium(self, stadium_id: int, name: Optional[str] = None,
                       city: Optional[str] = None, country_id: Optional[int] = None) -> Stadium:
        """Updatea stadium's information with validation."""
        existing = self.repository.get_by_id(stadium_id)
        if not existing:
            raise ValueError(f"Stadium with ID {stadium_id} not found.")

        updated = self.repository.update(
            stadium_id=stadium_id,
            name=name,
            city=city,
            country_id=country_id
        )

        if not updated:
            raise ValueError("Failed to update stadium.")
        return updated

    def delete_stadium(self, stadium_id: int) -> bool:
        """Delete a stadium by ID after validating existence."""
        existing = self.repository.get_by_id(stadium_id)
        if not existing:
            raise ValueError(f"Stadium with ID {stadium_id} not found.")

        return self.repository.delete(stadium_id)
