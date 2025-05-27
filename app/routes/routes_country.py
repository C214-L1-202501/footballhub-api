from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.services.CountryService import CountryService
from app.schemas.country import Country
from app.schemas.stadium import Stadium
from app.schemas.player import Player
from app.schemas.team import Team

router = APIRouter(
    prefix="/country",
    tags=["country"],
)

country_service = CountryService()


@router.get("/", response_model=List[Country])
async def get_all_countries():
    return country_service.get_all_countries()


@router.get("/{country_id}")
async def get_country(country_id: int):
    country = country_service.find_country_by_id(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.post("/", status_code=201)
async def add_country(country_input: Country):
    country = country_service.create_country(country_input.name)
    return country

@router.post("/list/", status_code=201, response_model=List[Country])
async def add_countries(countries: List[Country]):
    try:
        created_countries = [country_service.create_country(c.name) for c in countries]
        return created_countries
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{country_id}")
async def update_country(country_id: int, country: Country):
    country = country_service.update_country(country_id, country.name)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.delete("/{country_id}")
async def delete_country(country_id: int):
    country = country_service.delete_country(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.get("/{country_id}/teams", response_model=List[Team])
async def get_teams_by_country(country_id: int):
    teams = country_service.get_teams_by_country(country_id)
    if teams is None:
        raise HTTPException(status_code=404, detail="Country not found or no teams")
    return teams

@router.get("/{country_id}/players", response_model=List[Player])
async def get_players_by_country(country_id: int):
    players = country_service.get_players_by_country(country_id)
    if players is None:
        raise HTTPException(status_code=404, detail="Country not found or no players")
    return players

@router.get("/{country_id}/stadiums", response_model=List[Stadium])
async def get_stadiums_by_country(country_id: int):
    stadiums = country_service.get_stadiums_by_country(country_id)
    if stadiums is None:
        raise HTTPException(status_code=404, detail="Country not found or no stadiums")
    return stadiums