from typing import List
from app.schemas.stadium import Stadium
from app.repositories.stadiumRepository import StadiumRepository

class StadiumService:
    def __init__(self, repository: StadiumRepository):
        self.repository = repository

    def find_stadium_by_id(self, stadium_id: int) -> Stadium:
        """Find a stadium by its ID."""
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise Exception("Estádio não encontrado.")
        return stadium

    def create_stadium(self, name: str, city: str, country_id: int) -> Stadium:
        """Create a new stadium."""
        self.validate_stadium_creation(name, city, country_id)
        return self.repository.create(name, city, country_id)

    def get_all_stadiums(self) -> List[Stadium]:
        """Retrieve all stadiums from the database."""
        return self.repository.get_all()

    def update_stadium(self, stadium_id: int, name: str = None, city: str = None, country_id: int = None) -> Stadium:
        """Update an existing stadium's information."""
        self.validate_stadium_update(name, city, country_id)
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise Exception("Estádio não encontrado.")
        return self.repository.update(stadium_id, name, city, country_id)

    def delete_stadium(self, stadium_id: int) -> bool:
        """Delete a stadium by its ID."""
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise Exception("Estádio não encontrado.")
        return self.repository.delete(stadium_id)

    def validate_stadium_creation(self, name: str, city: str, country_id: int):
        """Validate the stadium creation data."""
        if len(name) < 3:
            raise Exception("O nome do estádio deve ter pelo menos 3 caracteres.")
        if len(city) < 3:
            raise Exception("A cidade do estádio deve ter pelo menos 3 caracteres.")
        # Aqui você pode adicionar validações adicionais, como checar se o país existe no banco de dados

    def validate_stadium_update(self, name: str, city: str, country_id: int):
        """Validate the stadium update data."""
        if name and len(name) < 3:
            raise Exception("O nome do estádio deve ter pelo menos 3 caracteres.")
        if city and len(city) < 3:
            raise Exception("A cidade do estádio deve ter pelo menos 3 caracteres.")
        # Adicione mais validações se necessário
