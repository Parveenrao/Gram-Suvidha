from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.announcement import AnnouncementTypeEnum


# When Head/Sarpanch of village wants to publish  announcement of event

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    type: AnnouncementTypeEnum = AnnouncementTypeEnum.general

 
class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[AnnouncementTypeEnum] = None


# What we send back 
 
class AnnouncementResponse(BaseModel):
    id: int
    village_id: int
    title: str
    content: str
    type: AnnouncementTypeEnum
    published_by: int
    created_at: datetime

    class Config:
        from_attributes = True