from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.services.teamService import TeamService
from app.schemas.team import Team
from app.schemas.player import Player

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)

team_service = TeamService()

@router.post("/", response_model=Team, status_code=201)
async def add_team(team_input: Team):
    """Create a new team"""
    try:
        team = team_service.create_team(
            name=team_input.name,
            country_id=team_input.country_id,
            nickname=team_input.nickname,
            city=team_input.city,
            founding_date=team_input.founding_date
        )
        return team
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    except IntegrityError as e:
        detail = "Erro de dados: "
        if "foreign key constraint" in str(e.orig):
            detail += "País não existe"
        elif "unique constraint" in str(e.orig):
            detail += "Time já cadastrado"
        else:
            detail += "Dados inválidos"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar time: {str(e)}"
        )

@router.get("/", response_model=List[Team])
async def get_all_teams():
    """Get all teams"""
    try:
        return team_service.get_all_teams()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar times: {str(e)}"
        )

@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: int):
    """Get a specific team by ID"""
    try:
        team = team_service.get_team(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        return team
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar time: {str(e)}"
        )

@router.put("/{team_id}", response_model=Team)
async def update_team(team_id: int, team: Team):
    """Update team information"""
    try:
        updated_team = team_service.update_team(
            team_id=team_id,
            name=team.name,
            country_id=team.country_id,
            nickname=team.nickname,
            city=team.city,
            founding_date=team.founding_date
        )
        if not updated_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        return updated_team
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de dados: Verifique os IDs e constraints"
        )
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar time: {str(e)}"
        )

@router.delete("/{team_id}")
async def delete_team(team_id: int):
    """Delete a team"""
    try:
        deleted = team_service.delete_team(team_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        return {"message": "Team deleted successfully"}
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir time: {str(e)}"
        )

@router.get("/{team_id}/players", response_model=List[Player])
async def get_players_by_team(team_id: int):
    """Get all players from a team"""
    try:
        players = team_service.get_players_by_team(team_id)
        if not players:  # Se quiser retornar 404 quando não houver jogadores
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No players found for this team"
            )
        return players
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar jogadores: {str(e)}"
        )
