from typing import List
from fastapi import APIRouter, Query
from app.services.CountryService import CountryService
from app.schemas.country import Country

router = APIRouter(
    prefix="/country",
    tags=["country"],
)

country_service = CountryService()

@router.get("/", response_model= List[Country])
async def get_all_countries():
    return country_service.get_all_countries()

@router.get("/{country_id}")
async def get_country(country_id: int):
    country = country_service.find_country_by_id(country_id)
    return country

@router.post("/", status_code=201)
async def add_country(country_input: Country):
    country = country_service.create_country(country_input)   
    return country

@router.put("/{country_id}")
async def update_country(country_id: int, country: Country):
    country = country_service.update_country(country_id, country)
    return country

@router.delete("/{country_id}")
async def delete_country(country_id: int):
    country = country_service.delete_country(country_id)
    return country