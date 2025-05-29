from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv

from app.schemas.team import Team
from app.schemas.team import ChampionshipParticipation
from app.schemas.player import Player


class TeamRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, name: str, country_id: int, nickname: Optional[str] = None, city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Team:
        """Create a new team in database."""
        with self._get_session() as session:
            team = Team(name=name, country_id=country_id, nickname=nickname, city=city, founding_date=founding_date)
            session.add(team)
            session.commit()
            session.refresh(team)
            return team

    def get_by_id(self, team_id: int) -> Optional[Team]:
        """Search for a team by its ID."""
        with self._get_session() as session:
            team = session.get(Team, team_id)
            return team

    def get_by_name(self, name: str) -> Optional[Team]:
        """Search for a team by its name."""
        with self._get_session() as session:
            statement = select(Team).where(Team.name == name)
            team = session.exec(statement).first()
            return team

    def get_all(self) -> List[Team]:
        """Returns all teams in database."""
        with self._get_session() as session:
            statement = select(Team)
            teams = session.exec(statement).all()
            return teams

    def update(self, team_id: int, name: Optional[str] = None, country_id: Optional[int] = None, nickname: Optional[str] = None, city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Optional[Team]:
        """Update the information of an existing team."""
        with self._get_session() as session:
            team = session.get(Team, team_id)
            if team:
                if name:
                    team.name = name
                if country_id:
                    team.country_id = country_id
                if nickname:
                    team.nickname = nickname
                if city:
                    team.city = city
                if founding_date:
                    team.founding_date = founding_date
                session.add(team)
                session.commit()
                session.refresh(team)
                return team
            return None

    def delete(self, team_id: int) -> bool:
        """Delete a team by its ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            team = session.get(Team, team_id)
            if team:
                session.delete(team)
                session.commit()
                return True
            return False
        
    def get_players(self, team_id: int) -> List[Player]:
        """Retorna todos os jogadores de um time."""
        with self._get_session() as session:
            statement = select(Player).where(Player.team_id == team_id)
            players = session.exec(statement).all()
            return players
   
    def create_championshipParticipation(self, championship_id: int = None, team_id: int = None, season: Optional[str] = None) -> ChampionshipParticipation:
        """Create a new team in database."""
        with self._get_session() as session:
            participation = ChampionshipParticipation(championship_id=championship_id, team_id=team_id, season=season)
            session.add(participation)
            session.commit()
            session.refresh(participation)
            return participation 
    
    def delete_championshipParticipation(self, championshipParticipation_id: int) -> bool:
        """Delete a participation by its ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            participation = session.get(ChampionshipParticipation, championshipParticipation_id)
            if participation:
                session.delete(participation)
                session.commit()
                return True
            return False