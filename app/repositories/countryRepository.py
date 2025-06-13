from typing import List, Optional
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv

from app.schemas.country import Country
from app.schemas.stadium import Stadium
from app.schemas.player import Player
from app.schemas.team import Team


class CountryRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, name: str) -> Country:
        """Create a new country in database."""
        with self._get_session() as session:
            country = Country(name=name)
            session.add(country)
            session.commit()
            session.refresh(country)
            return country

    def get_by_id(self, country_id: int) -> Optional[Country]:
        """Search for a country by its ID."""
        with self._get_session() as session:
            country = session.get(Country, country_id)
            return country

    def get_by_name(self, name: str) -> Optional[Country]:
        """Search for a country by its name."""
        with self._get_session() as session:
            statement = select(Country).where(Country.name == name)
            country = session.exec(statement).first()
            return country

    def get_all(self) -> List[Country]:
        """Returns all countries in database."""
        with self._get_session() as session:
            statement = select(Country)
            countries = session.exec(statement).all()
            return countries

    def update(self, country_id: int, name: str) -> Optional[Country]:
        """Update the name of an existing country."""
        with self._get_session() as session:
            country = session.get(Country, country_id)
            if country:
                country.name = name
                session.add(country)
                session.commit()
                session.refresh(country)
                return country
            return None

    def delete(self, country_id: int) -> bool:
        """Delete a country by its ID. Returns Tue if successful, False if not found."""
        with self._get_session() as session:
            country = session.get(Country, country_id)
            if country:
                session.delete(country)
                session.commit()
                return True
            return False
    def get_teams(self, country_id: int) -> List[Team]:
        """Retorna todos os times de um país."""
        with self._get_session() as session:
            statement = select(Team).where(Team.country_id == country_id)
            teams = session.exec(statement).all()
            return teams

    def get_players(self, country_id: int) -> List[Player]:
        """Retorna todos os jogadores de um país."""
        with self._get_session() as session:
            statement = select(Player).where(Player.country_id == country_id)
            players = session.exec(statement).all()
            return players

    def get_stadiums(self, country_id: int) -> List[Stadium]:
        """Retorna todos os estádios de um país."""
        with self._get_session() as session:
            statement = select(Stadium).where(Stadium.country_id == country_id)
            stadiums = session.exec(statement).all()
            return stadiums