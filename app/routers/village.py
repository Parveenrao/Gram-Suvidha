from fastapi import Depends  , HTTPException , status , APIRouter
from app.schema.village import VillageCreate , VillageResponse , VillageUpdate
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session
from typing import List
from app.models.user import RoleEnum
from app.models.villages import Village
from app.database import get_db
from app.utils.exception import ConflictException  , NotFoundException , UnauthorizeException , ForbiddenException ,  BadRequestException

router = APIRouter()


#-------------------Public Endpoints-------------------------------

# Get all villages 

@router.get("/villages" , response_model=List[VillageResponse])

def get_all_villages(db : Session = Depends(get_db)):
    
    # get all registered villages 
    
    villages = db.query(Village).all()
    
    if not villages:
        raise NotFoundException("No village found")
    
    return villages


@router.get("/villages/{village_id}" , response_model=VillageResponse)

def get_village(village_id : int , db : Session = Depends(get_db)):
    
    village = db.query(Village).filter(Village.id == village_id).first()
    
    if not village:
        raise NotFoundException("Village not found")
    
    return village


#---------------------- Admin Only Endpoints---------------------------------------

# Register a new village

@router.post("/register-village" , response_model=VillageResponse , status_code=201)

def create_village(data : VillageCreate , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # Admin --> can register village
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can create villages")
    
    # check if villages already registered
    
    existing = db.query(Village).filter(Village.name == data.name , Village.district == data.district).first()
    
    if existing:
        raise ConflictException("Village already registered")
    
    village = Village(name = data.name,
                      district = data.district,
                      state = data.state,
                      pincode = data.pincode)
    
    db.add(village)
    db.commit()
    db.refresh(village)
    
    return village

# update village detail 

@router.patch("{village_id}" , response_model=VillageResponse)

def update_village(village_id : int  , data : VillageUpdate , current_user = Depends(get_current_user) , db:Session = Depends(get_db)):
    
    # Admin only -> only admin can create villages 
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can update village")
    
    village = db.query(Village).filter(Village.id == village_id).first()
    
    if not village:
        raise NotFoundException("Village not found")
    
    # Only update fields that are sent — leave rest unchanged
    
    for key , value in data.model_dump(exclude_unset=True).items():
        setattr(village , key , value)
        
    db.commit()
    db.refresh(village)
    
    return village



# Delete village by id 

@router.delete("{village_id}")

def delete_village(village_id : int , db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    # Admin only --> delete a village permanently 
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can delete village")
    
    village = db.query(Village).filter(Village.id == village_id).first()
    
    if not village:
        raise NotFoundException("Village not found")
    
    db.delete(village)
    db.commit()
    
    return {"message": f"Village '{village.name}' deleted successfully"}    
        