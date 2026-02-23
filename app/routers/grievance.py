from fastapi import HTTPException , Depends , status , APIRouter
from app.database import get_db
from typing import List
from app.utils.auth import get_current_user
from app.utils.exception import NotFoundException , ForbiddenException , BadRequestException , ConflictException , UnauthorizeException
from app.models.grievance import Grievance , GrievanceStatusEnum
from app.models.user import RoleEnum
from datetime import datetime
from sqlalchemy.orm import Session
from app.schema.grievance import GrievanceCreate , GrievanceReply , GrievanceResponse

router = APIRouter()


#----------------------------Public Endpoints----------------------------

@router.post("/submit_grievance" , response_model=GrievanceResponse , status_code=201)

def submit_grievance(data : GrievanceCreate , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    Submit a new grievance/complaint.
    Any logged in citizen can submit.
    Status starts as 'open' automatically.
    """
    
    greivance  = Grievance(title = data.title,
                           description = data.description,
                           category = data.category,
                           village_id = current_user.village_id,
                           citizen_id  = current_user.citizen_id , 
                           status = GrievanceStatusEnum.open,        # always open on submit
                           sarpanch_reply = None,
                            resolved_at = None)
    
    db.add(greivance)
    db.commit()
    db.refresh(greivance)
    
    return greivance


# Get My Greivance 

@router.get("/my" , response_model=List[GrievanceResponse])

def get_my_grievance(db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    Get all grievances submitted by logged in citizen.
    Citizens can only see their own grievances.
    """
    
    grievance = db.query(Grievance).filter(Grievance.citizen_id == current_user.id).order_by(Grievance.created_at.desc()).all()
    
    return grievance

# Get grievance by id 
@router.get("/{grievance}" , response_model= GrievanceResponse)
def get_grievace_id(grievance_id :int , db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    """
    Get single grievance of logged in citizen.
    Citizen can only view their own grievance.
    """
    
    greivance = db.query(Grievance).filter(Grievance.id == grievance_id , Grievance.citizen_id == current_user.id).first()
    
    if not greivance:
        raise NotFoundException("No Grievance Found")
    
    return greivance


# Delete my grievance 

@router.delete("/my/{grievance_id}" , response_model=GrievanceResponse)

def delete_grievance(grievance_id : int , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    Citizen can delete their own grievance.
    Only allowed if status is still 'open'.
    Cannot delete if sarpanch already replied.
    """
    
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id , Grievance.citizen_id == current_user.id).first()
    
    if not grievance:
        raise NotFoundException('Grievance not found')
    
    # cannot delete if grievance in progress or resolved
    
    if grievance.status != GrievanceStatusEnum.open:
        raise BadRequestException("Cannot delete grievance that is already in progress or resolved")
    
    
    db.delete(grievance)
    db.commit()
    
    return {"message": "Grievance deleted successfully ✅"}


#--------------------------- Admin Endpoints------------------------------------

# Get all grievance

@router.get("/all" , response_model=List[GrievanceResponse])

def get_all_grievance(db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Get all grievances of the village.
    Ordered by latest first.
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied , Only Sarpanch can see all the grievance")
    
    greivances = db.query(Grievance).filter(Grievance.village_id == current_user.village_id).order_by(Grievance.created_at.desc()).all()
    
    return greivances


# Get Grievnace by status 

@router.get("/all/status/{status}" , response_model=List[GrievanceResponse])

def get_grievance_by_status(status : GrievanceStatusEnum , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Filter grievances by status.
    Example: /api/grievances/all/status/open
    Returns: open / in_progress / resolved / rejected
    """
    
    if current_user.role not in [RoleEnum.admin , RoleEnum.sarpanch]:
        raise ForbiddenException("Acess Denied ")
    
    
    grievance = db.query(Grievance).filter(Grievance.village_id == current_user.village_id , Grievance.status == status).order_by(
                                                                        Grievance.created_at.desc()
    ).all()
    
    return grievance

# Get Full details of any grievance

@router.get("/all/{grievance_id}" , response_model=GrievanceResponse)

def get_detail_grievance(grievance_id : int , db : Session  = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Get full details of any grievance.
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id , Grievance.village_id == current_user.village_id).first()
    
    if not grievance:
        raise NotFoundException("Grievance not found")
    
    return grievance

# Change status of Grievance or reply to Grievance

@router.patch("/all/{grievance}/status" , response_model=GrievanceResponse)

def reply_to_grievance(grievance_id : int , data : GrievanceReply , db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Reply to a grievance and update status.
    If status is 'resolved' → resolved_at timestamp is set automatically.
    """
    
    if current_user.role not in [RoleEnum.admin , RoleEnum.sarpanch]:
        raise ForbiddenException('Access Denied')
    
    grievance = db.query(Grievance).filter(Grievance.village_id == grievance_id , Grievance.village_id == current_user.village_id).first()
    
    if not grievance:
        raise NotFoundException("Grievance not found")
    
    # cannot reply to resolved or rejected grievance
    
    if grievance.status not in [GrievanceStatusEnum.resolved , GrievanceStatusEnum.rejected]:
        raise BadRequestException('Grievance is already solved , Cannot update again')
    
    grievance.sarpanch_reply = data.sarpanch_reply
    
    grievance.status = data.status
    
    # Set resolved timestamp automatically
    
    if grievance.status == GrievanceStatusEnum.resolved:
        grievance.resolved_at = datetime.now()
        
    
    db.commit()
    db.refresh(grievance)
    
    return grievance    


# Summary of all Grievance 

@router.get("/all/summary/count")

def get_grievance_summary(db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    SARPANCH / ADMIN ONLY — Get count summary of all grievances.
    Shows how many are open, in progress, resolved, rejected.
    Useful for sarpanch dashboard.
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin]:
        raise ForbiddenException("Access Denied")
    
    total = db.query(Grievance).filter(Grievance.village_id == current_user.village_id).count()
    open_count = db.query(Grievance).filter(Grievance.village_id == current_user.village_id , Grievance.status == GrievanceStatusEnum.open).count()
    progress_count = db.query(Grievance).filter(Grievance.village_id == current_user.village_id , Grievance.status == GrievanceStatusEnum.in_progress).count()
    resolved_count = db.query(Grievance).filter(Grievance.village_id == current_user.village_id , Grievance.status == GrievanceStatusEnum.resolved).count()
    rejected_count  = db.query(Grievance).filter(Grievance.village_id == current_user.village_id , Grievance.status == GrievanceStatusEnum.rejected).count()
    
    
    return {
        
        "total": total,
        "open": open_count,
        "in_progress": progress_count,
        "resolved": resolved_count,
        "rejected": rejected_count
        
    }
    