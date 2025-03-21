from typing import List, Optional
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv
from datetime import datetime

from app.schemas.player import Player


class PlayerRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, name: str, birth_date: Optional[datetime], country_id: int, position_id: int, team_id: Optional[int] = None) -> Player:
        """Create a new player in the database."""
        with self._get_session() as session:
            player = Player(
                name=name,
                birth_date=birth_date,
                country_id=country_id,
                position_id=position_id,
                team_id=team_id
            )
            session.add(player)
            session.commit()
            session.refresh(player)
            return player

    def get_by_id(self, player_id: int) -> Optional[Player]:
        """Search for a player by their ID."""
        with self._get_session() as session:
            player = session.get(Player, player_id)
            return player

    def get_by_name(self, name: str) -> Optional[Player]:
        """Search for a player by their name."""
        with self._get_session() as session:
            statement = select(Player).where(Player.name == name)
            player = session.exec(statement).first()
            return player

    def get_all(self) -> List[Player]:
        """Returns all players in the database."""
        with self._get_session() as session:
            statement = select(Player)
            players = session.exec(statement).all()
            return players

    def update(self, player_id: int, name: Optional[str] = None, birth_date: Optional[datetime] = None, country_id: Optional[int] = None, position_id: Optional[int] = None, team_id: Optional[int] = None) -> Optional[Player]:
        """Update an existing player's information."""
        with self._get_session() as session:
            player = session.get(Player, player_id)
            if player:
                if name:
                    player.name = name
                if birth_date:
                    player.birth_date = birth_date
                if country_id:
                    player.country_id = country_id
                if position_id:
                    player.position_id = position_id
                if team_id:
                    player.team_id = team_id
                session.add(player)
                session.commit()
                session.refresh(player)
                return player
            return None

    def delete(self, player_id: int) -> bool:
        """Delete a player by their ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            player = session.get(Player, player_id)
            if player:
                session.delete(player)
                session.commit()
                return True
            return False
