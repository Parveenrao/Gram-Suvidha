from pydantic import BaseModel
from pydantic import Field
from typing import Optional , List
from datetime import datetime 
from app.models.grievance import GrievanceStatusEnum


# When citizen want to submit a complaint/grievance

class GrievanceCreate(BaseModel):
    title : str                      # Required - No water supply in ward 2 
    description : str                # Reuired  - No water supply from last three days 
    category : str                   # Required - Road / Water / electricity
    
    
    
# When Sarpanch Wants to give reply 

class GrievanceReply(BaseModel):
    sarpanch_reply : str            # Required -- We fixed the pipeline    
    status         : GrievanceStatusEnum # Required -- Resolved  / In_progress / Rejected
    
    
# What we send back 

class GrievanceResponse(BaseModel):
    id: int                        # auto — 1, 2, 3...
    village_id: int                # which village
    citizen_id: int                # who submitted
    title: str                     # "No water supply in Ward 2"
    description: str               # full problem description
    category: str                  # "water"
    status: GrievanceStatusEnum    # "resolved"
    sarpanch_reply: Optional[str]  # null until sarpanch replies
    created_at: datetime           # when submitted
    resolved_at: Optional[datetime] # null until resolved

    class Config:
        from_attributes = True    