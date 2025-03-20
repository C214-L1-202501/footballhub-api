from typing import List, Optional
from app.schemas.entities.Country import Country

class CountryRepository:
    def __init__(self):
        self.__countries: List[Country] = []

    def save(self, country: Country) -> Country:
        self.__countries.append(country)
        return country

    def find_all(self) -> List[Country]:
        return self.__countries

    def delete(self, name: str) -> Optional[Country]:
        for country in self.__countries:
            if country.name == name:
                self.__countries.remove(country)
                return country
        return None
