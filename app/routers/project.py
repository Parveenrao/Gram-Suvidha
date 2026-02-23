from fastapi import HTTPException , APIRouter , Depends , UploadFile , File 
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project , ProjectStatusEnum
from app.models.user import RoleEnum
from app.schema.project import ProjectCreate  , ProjectUpdate , ProjectResponse
from app.utils.auth import get_current_user
from app.utils.exception import ConflictException  , NotFoundException , UnauthorizeException , ForbiddenException ,  BadRequestException

router = APIRouter()


#----------------------------- Public Endpoints-----------------------


# Get all projects 

@router.get("/projects" , response_model = List[ProjectResponse])

def get_all_projects(village_id : int ,db: Session = Depends(get_db)):
    
    """
    
    Get all projects of a village.
    Public --> citizens can see all projects.
    Filter by village_id as query param.
    Example: /api/projects/?village_id=1
    """
    
    projects = db.query(Project).filter(Project.village_id == village_id).order_by(Project.created_at.desc()).all()
    
    if not projects:
        raise NotFoundException("NO Projects Found")
    
    return projects 

# Get Project status 


@router.get("/status{status}" , response_model=ProjectResponse)

def get_project_status(status : ProjectStatusEnum , village_id : int , db: Session = Depends(get_db)):
    
    """
    Get projects filtered by status.
    Example: /api/projects/status/ongoing?village_id=1
    Returns: planned / ongoing / completed / cancelled projects
    """
    
    projects = db.query(Project).filter(Project.village_id == village_id , Project.status == status).all()
    
    return projects


# Get project by project_id 

@router.get("/{project_id}" , response_model=ProjectResponse)

def get_project(project_id : int , db:Session = Depends(get_db)):
    
    """
    Get single project detail by ID
    Public --> Any one view
    """
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise NotFoundException("Project not found")
    
    
#---------------------------------- Sarpanch / Head / Ward Member  Endpoints-------------------------

# Create project

@router.post("/create-project" , response_model=ProjectResponse)

def create_project(data : ProjectCreate , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """ 
    Create a new work / Project
    Allowed -> Sarpanch / Ward member / Admin
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin , RoleEnum.ward_citizen]:
        raise ForbiddenException("Only Sarpanch Or Ward Member create projects")
    
    # Ward member create project for their ward only 
    
    if current_user.role == RoleEnum.ward_citizen:
        if data.ward_number != current_user.ward_number:
            raise ForbiddenException("Ward memeber can only create project for their own ward {current_user.ward_number}")
    
    project = Project(title = data.title,
                      description = data.description,
                      category = data.category,
                      ward_number = data.ward_number,
                      estimated_cost = data.estimated_cost,
                      start_data = data.start_date,
                      end_date = data.end_date,
                      created_by = current_user.id,
                      village_id = current_user.village_id,
                      photos = []                               # Empty list of photos intially
                      )    
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project

# Update project detail 

@router.patch("/{project_id}" , response_model=ProjectResponse)

def update_project(project_id : int , data : ProjectUpdate , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    """
    Update project detail or status
    Allowed -> sarpanch , admin , ward(own wards)
    """
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin , RoleEnum.ward_citizen]:
        raise ForbiddenException("Acess Denied")
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise NotFoundException("Project Not found")
    
    
    # Ward member can update thier own ward projects 
    
    if current_user.role == RoleEnum.ward_citizen:
        if project.ward_number != current_user.ward_number:
            raise ForbiddenException("Ward member can only update project of their own wards")
    
    for key , value in data.model_dump(exclude_unset=True).items():
        setattr(project , key , value)
        
    db.commit()
    db.refresh(project)
    
    return project

# Update status of project 

@router.patch("/{project_id}/status" , response_model=ProjectResponse)

def update_project_status(project_id : int , payload : ProjectUpdate , db:Session = Depends(get_db), 
                          current_user = Depends(get_current_user)):
    
    
    # Qucik status update for a project 
    # Allowed - Sarpanch , ward member , admin
    
    # Role check 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin , RoleEnum.ward_citizen]:
        raise ForbiddenException("Access Denied")
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise NotFoundException("Project not found")
    
    
    if payload.status is None:
        raise BadRequestException("status is required")
    
    
    # update status 
    
    project.status = payload.status
    
    db.commit()
    db.refresh(project)
    
    return project
              

# Delete Project

@router.delete("/{project_id}" , response_model=ProjectResponse)
    
def delete_project(project_id : int , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # Only admin can delete project
    
    # Role check 
    
    if current_user.role not in [RoleEnum.sarpanch , RoleEnum.admin , RoleEnum.ward_citizen]:
        raise ForbiddenException("Access Denied")
    
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise NotFoundException("Project not found")
    
    db.delete(project)
    db.commit()
    
    return {
        "success": True,
        "message": f"Project '{project.title}' deleted successfully"
    }
    
    
    
    
    
    
    