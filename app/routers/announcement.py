from fastapi import HTTPException , APIRouter , Depends , UploadFile , File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.announcement import Announcement , AnnouncementTypeEnum
from app.models.user import RoleEnum
from app.schema.announcement import AnnouncementCreate , AnnouncementResponse , AnnouncementTypeEnum , AnnouncementUpdate
from app.utils.auth import get_current_user
from app.utils.exception import ConflictException  , NotFoundException , UnauthorizeException , ForbiddenException ,  BadRequestException

router = APIRouter()



#------------------------------------- Public Endpoints---------------------------

# Get all announcement of village 

@router.get("/Get" , response_model= List[AnnouncementResponse])

def get_all_announcement(viilage_id : int , db : Session = Depends(get_db)):
    
    """  Get all announcements of a village.
    Public — any citizen can view.
    Ordered by latest first.
    Example: /api/announcements/?village_id=1"""
    
    announcments = db.query(Announcement).filter(Announcement.village_id == viilage_id).order_by(Announcement.created_at.desc()).all()
    
    return announcments


# Get announcement by type 

@router.get("/type/{ann_type}" , response_model=List[AnnouncementResponse])

def get_announcement_by_type(village_id : int , ann_type : AnnouncementTypeEnum , db : Session = Depends(get_db)):
    
    """
    Get announcements filtered by type.
    Example: /api/announcements/type/scheme?village_id=1
    Types: notice / scheme / meeting / alert / general
    """
    
    announcement = db.query(Announcement).filter(Announcement.village_id == village_id , Announcement.type == ann_type).order_by(
        Announcement.created_at.desc()).all()
    
    return announcement

# Get latest announcement 

@router.get("/latest" , response_model=List[AnnouncementResponse])

def get_latest_announcement(village_id : int , limit : int = 5 , db:Session = Depends(get_db)):
    
    """
    Get latest N announcements.
    Default limit is 5.
    Used for home page/dashboard.
    Example: /api/announcements/latest?village_id=1&limit=5
    """
    
    announcement = db.query(Announcement).filter(Announcement.village_id == village_id).order_by(Announcement.created_at.desc()).limit(limit).all()
    
    return announcement

# Get announcement by id 

@router.get("/{announcement_id}" , response_model=AnnouncementResponse)

def get_announcement(announcement_id : int , db : Session = Depends(get_db)):
    
    """
    Get single announcement by ID.
    Public — anyone can view.
    """
    
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    
    if not announcement:
        raise NotFoundException("Announcement not found")
    
    return announcement

#---------------------------------- Admin Endpoints ------------------------------------

# Create announcement 

@router.post("/create" , response_model=AnnouncementResponse , status_code=201)

def create_announcement(data : AnnouncementCreate , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Publish a new announcement.
    village_id and published_by added automatically from logged in user.
    """
    
    if get_current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
     
    announcement = Announcement(title = data.title,
                                 content = data.content,
                                 type = data.type,
                                 village_id = current_user.viilage_id,
                                 published_by = current_user.id)
    
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    
    return announcement
     
# Update an announcement 

@router.patch("/{announcement_id}" , response_model=AnnouncementResponse)

def admin_update_announcement(announcement_id : int , data : AnnouncementUpdate , 
                              db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # Admin check 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id , Announcement.village_id == current_user.village_id).first()
    
    if not announcement:
        raise NotFoundException("Announcement not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise BadRequestException("No Fields provided")
    
    # Apply updated 
    
    for key , value in update_data.items():
        setattr(announcement , key , value)
    
    
    db.commit()
    db.refresh(announcement)
    
    return announcement


# Delete an announcement 

@router.delete("/{announcement_id}" , response_model=AnnouncementResponse)

def delete_announcement(announcement_id : int , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Delete an announcement.
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id , Announcement.village_id == current_user.village_id).first()
    
    if not announcement:
        raise NotFoundException("Announcement not found")
    
    db.delete(announcement)
    db.commit()
    
    return {"message" : f"Announcement {announcement.title} deleted successfully"}     


# Get summary of an announcement 

@router.get("/summary/count")

def get_announcement_summary(db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """ Only admin can see summary"""
    
    # check role 
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    rows = db.query(Announcement.type ,func.count(Announcement.id)).filter(Announcement.village_id == current_user.village_id).group_by(
        Announcement.type).all()
    
    summary = {"total": 0}

    # initialize all enum types to 0
    for ann_type in AnnouncementTypeEnum:
        summary[ann_type.value] = 0

    # fill actual counts
    for ann_type, count in rows:
        summary[ann_type.value] = count
        summary["total"] += count

    return summary