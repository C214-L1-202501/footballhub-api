from typing import List, Optional
from app.schemas.entities.Country import Country
from app.repositories.CountryRepository import CountryRepository

class CountryService:
    def __init__(self, repository: CountryRepository):
        self.__repository = repository

    def add_country(self, name: str) -> Country:
        country = Country(name)
        return self.__repository.save(country)

    def list_country(self) -> List[Country]:
        return self.__repository.find_all()

    def remove_country(self, name: str) -> Optional[Country]:
        return self.__repository.delete(name)
