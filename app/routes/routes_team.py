from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.services.teamService import TeamService
from app.schemas.team import Team
from app.schemas.team import ChampionshipParticipation
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
@router.post(
    "/{team_id}/participations", 
    response_model=ChampionshipParticipation,
    status_code=status.HTTP_201_CREATED
)

@router.post(
    "/{team_id}/participations", 
    response_model=ChampionshipParticipation,
    status_code=status.HTTP_201_CREATED
)
async def create_participation(
    team_id: int,
    participation: ChampionshipParticipation
):
    """
    Adiciona um time a um campeonato (cria participação)
    """
    try:
        return team_service.create_championship_participation(
            championship_id=participation.championship_id,
            team_id=team_id,
            season=participation.season
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        detail = "Erro de dados: "
        if "foreign key constraint" in str(e.orig):
            detail += "Time ou campeonato não existe"
        elif "unique constraint" in str(e.orig):
            detail += "Time já está registrado neste campeonato"
        else:
            detail += "Dados inválidos"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar participação: {str(e)}"
        )
@router.delete(
    "/participations/{participation_id}",
    status_code=status.HTTP_200_OK
)
async def delete_participation(participation_id: int):
    """
    Remove uma participação de time em campeonato
    """
    try:
        success = team_service.delete_championship_participation(participation_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participação não encontrada"
            )
            
        return {"message": "Participação removida com sucesso"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover participação: {str(e)}"
        )
@router.get("/{team_id}/participations")
async def get_participations_by_team(team_id: int):
    """
    Lista todas as participações de campeonato de um time, incluindo nome e ano do campeonato.
    """
    try:
        participations = team_service.get_participations_by_team(team_id)
        if not participations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma participação encontrada para este time"
            )
        return participations  # Retorna lista de dicts, cada um já com os campos extras
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar participações: {str(e)}"
        )