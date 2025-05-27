from typing import List
from fastapi import APIRouter, HTTPException
from app.services.stadiumService import StadiumService
from app.schemas.stadium import Stadium

router = APIRouter(
    prefix="/stadiums",  # Changed from "/stadium" to "/stadiums" for RESTful convention
    tags=["stadiums"],   # Changed to plural for consistency
)

stadium_service = StadiumService()

@router.post("/", response_model=Stadium, status_code=201)
async def add_stadium(stadium_input: Stadium):
    """Create a new stadium"""
    stadium = stadium_service.create_stadium(
        stadium_input.name,
        stadium_input.city,
        stadium_input.country_id)
    return stadium

@router.get("/", response_model=List[Stadium])
async def get_all_stadiums():
    """Get all stadiums"""
    return stadium_service.get_all_stadiums()

@router.get("/{stadium_id}", response_model=Stadium)
async def get_stadium(stadium_id: int):
    """Get a specific stadium by ID"""
    stadium = stadium_service.find_stadium_by_id(stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return stadium

@router.put("/{stadium_id}", response_model=Stadium)
async def update_stadium(stadium_id: int, stadium: Stadium):
    """Update stadium information"""
    updated_stadium = stadium_service.update_stadium(
        stadium_id=stadium_id,
        name=stadium.name,
        city=stadium.city,
        country_id=stadium.country_id
    )
    if not updated_stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return updated_stadium

@router.delete("/{stadium_id}")
async def delete_stadium(stadium_id: int):
    """Delete a stadium"""
    if not stadium_service.delete_stadium(stadium_id):
        raise HTTPException(status_code=404, detail="Stadium not found")
    return {"message": "Stadium deleted successfully"}