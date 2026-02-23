from pydantic import BaseModel
from pydantic import Field
from typing import Optional , List
from datetime import datetime 
from app.models.project import ProjectStatusEnum

# When Head/Sarpanch of village want to create a new work/project

class ProjectCreate(BaseModel):
    title : str                           # eg.  Road Repair Ward 3 
    description : Optional[str] = None    # optinal Repair of main road
    category : str                        # Required Road / Water / Sanitation
    ward_number : Optional[int] = None    # Optional which ward (2 ,3, 4)
    estimated_cost : float                # Required (150000 (1.5 lakhs))
    start_date : Optional[datetime] = None
    end_date :Optional[datetime] = None
    
    
# When Sarpanch updates progress

class ProjectUpdate(BaseModel):
    status : Optional[ProjectStatusEnum] = None
    acutal_cost : Optional[float] = None
    description : str = None
    
# What we send back 


class ProjectResponse(BaseModel):
    id: int                         # auto — 1, 2, 3...
    village_id: int                 # which village
    title: str                      # "Road Repair Ward 3"
    description: Optional[str]
    category: str                   # "road"
    ward_number: Optional[int]      # 3
    estimated_cost: float           # 150000.0
    actual_cost: float              # 145000.0 (after completion)
    status: ProjectStatusEnum       # "completed"
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    photos: List[str]               # ["https://cloudinary.com/photo1.jpg", ...]
    created_at: datetime

    class Config:
        from_attributes = True    