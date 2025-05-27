from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.player import Player, Position
from app.services.PlayerService import PlayerService

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

service = PlayerService()

@router.post(
    "/",
    response_model=Player,
    status_code=status.HTTP_201_CREATED
)
async def create_player(player_input: Player):
    try:
        return service.create_player(
            player_input.name,
            player_input.birth_date,
            player_input.country_id,
            player_input.position_id,
            player_input.team_id
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        detail = "Erro de dados: "
        if "foreign key" in str(e.orig):
            detail += "País, posição ou time inválido"
        elif "unique constraint" in str(e.orig):
            detail += "Jogador já existe"
        else:
            detail += "Dados inválidos"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=detail)
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar jogador: {str(e)}"
        )

@router.post(
    "/list/",
    response_model=List[Player],
    status_code=status.HTTP_201_CREATED
)
async def create_list(players: List[Player]):
    try:
        return service.create_players(players)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Erro de dados: Verifique IDs e unicidade"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar jogadores: {str(e)}"
        )

@router.get(
    "/",
    response_model=List[Player]
)
async def get_all_players():
    try:
        return service.get_all_players()
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar jogadores: {str(e)}"
        )

@router.get(
    "/{player_id}",
    response_model=Player
)
async def get_player(player_id: int):
    try:
        player = service.get_player(player_id)
        if not player:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Jogador não encontrado"
            )
        return player
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar jogador: {str(e)}"
        )

@router.put(
    "/{player_id}",
    response_model=Player
)
async def update_player(player_id: int, player_data: Player):
    try:
        updated_player = service.update_player(
            player_id=player_id,
            name=player_data.name,
            birth_date=player_data.birth_date,
            country_id=player_data.country_id,
            position_id=player_data.position_id,
            team_id=player_data.team_id
        )
        if not updated_player:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Jogador não encontrado"
            )
        return updated_player
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Erro de dados: Verifique os IDs fornecidos"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar jogador: {str(e)}"
        )

@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_player(player_id: int):
    try:
        deleted = service.delete_player(player_id)
        if not deleted:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Jogador não encontrado"
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir jogador: {str(e)}"
        )

@router.post(
    "/positions",
    response_model=List[Position],
    status_code=status.HTTP_201_CREATED
)
async def create_positions(positions: List[Position]):
    try:
        names = [p.name for p in positions]
        return service.create_positions(names)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Algumas posições já existem"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar posições: {str(e)}"
        )
