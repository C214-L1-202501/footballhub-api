from typing import List, Optional
from app.schemas.stadium import Stadium
from app.repositories.stadiumRepository import StadiumRepository


class StadiumService:
    def __init__(self):
        self.repository = StadiumRepository()

    def find_stadium_by_id(self, stadium_id: int) -> Stadium:
        """Find a stadium by its ID."""
        try:
            stadium = self.repository.get_by_id(stadium_id)
            if not stadium:
                raise Exception("Stadium not found.")
        except Exception as e:
            raise e
        return stadium
    
    def find_stadium_by_name(self, name: str) -> Stadium:
        """Find a stadium by its name."""
        try:
            # Note: You might need to add a get_by_name method to StadiumRepository
            stadium = self.repository.get_by_name(name)
            if not stadium:
                raise Exception("Stadium not found.")
        except Exception as e:
            raise e
        return stadium

    def create_stadium(self, name: str, city: str, country_id: int) -> Stadium:
        """Create a new stadium."""
        stadium = self.repository.create(name, city, country_id)
        return stadium

    def get_all_stadiums(self) -> List[Stadium]:
        """Retrieve all stadiums."""
        return self.repository.get_all()

    def update_stadium(self, stadium_id: int, name: Optional[str] = None, 
                      city: Optional[str] = None, country_id: Optional[int] = None) -> Stadium:
        """Update a stadium by its ID."""
        stadium = self.repository.update(stadium_id, name, city, country_id)
        if not stadium:
            raise Exception("Stadium not found.")
        return stadium

    def delete_stadium(self, stadium_id: int) -> bool:
        """Delete a stadium by its ID."""
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise Exception("Stadium not found.")
        return self.repository.delete(stadium_id)