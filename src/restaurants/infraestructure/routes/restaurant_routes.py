from datetime import time
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from src.shared.db.database import get_db

from typing import Annotated
from sqlmodel import Session, select

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/")
async def get_restaurants():
    """
    Get all restaurants.
    """
    return {"message": "List of restaurants"}