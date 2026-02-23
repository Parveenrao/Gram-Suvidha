from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# When admin want to register a new village

class VillageCreate(BaseModel):
    name: str
    district: str
    state: str
    pincode: str

# When admin want to update village details

class VillageUpdate(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


# what we send back

class VillageResponse(BaseModel):
    id: int
    name: str
    district: str
    state: str
    pincode: str
    created_at: datetime

    class Config:
        from_attributes = True