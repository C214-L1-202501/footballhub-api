from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path, Body
from app.services.ChampionshipService import ChampionshipService
from app.schemas.championship import Championship

router = APIRouter(
    prefix="/championship",
    tags=["championship"],
)

championship_service = ChampionshipService()


@router.post("/", status_code=201)
async def add_championship(championship_input: Championship):
    championship = championship_service.create_championship(
        championship_input.name,
        championship_input.country_id,
        championship_input.type,
        championship_input.season
    )
    return championship

@router.get("/", response_model=List[Championship])
async def get_all_championships():
    return championship_service.get_all_championships()

@router.get("/id/{championship_id}")
async def get_country(championship_id: int):
    championship = championship_service.find_championship_by_id(championship_id)
    if not championship:
        raise HTTPException(status_code=404, detail="Country not found")
    return championship

@router.get("/name/{championship_name}")
async def get_country(championship_name: str):
    championship = championship_service.find_championship_by_name(championship_name)
    if not championship:
        raise HTTPException(status_code=404, detail="Country not found")
    return championship

@router.put("/{championship_id}")
async def update_championship(championship_id: int, championship: Championship):
    updated_championship = championship_service.update_championship(
        championship_id,
        championship.name,
        championship.country_id,
        championship.type,
        championship.season
    )
    if not updated_championship:
        raise HTTPException(status_code=404, detail="Championship not found")
    return updated_championship


@router.delete("/{championship_id}")
async def delete_championship(championship_id: int):
    championship = championship_service.delete_championship(championship_id)
    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found")
    return championship
