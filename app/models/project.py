from sqlalchemy import Column , String , Enum , DateTime , ForeignKey , Integer , Float , JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ProjectStatusEnum(str , enum.Enum):
    planned = "planned"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"
    

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer , primary_key=True , index=True)
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    title = Column(String , nullable= False)
    description = Column(String , nullable=False)
    category  =  Column(String , nullable =  False)
    ward_number = Column(Integer , nullable=False)
    estimated_cost = Column(Float , nullable=False)
    actual_cost = Column(Float , default=0.0)
    status = Column(Enum(ProjectStatusEnum ,  name="project_status_enum") ,  default=ProjectStatusEnum.planned)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    photos = Column(JSON, default=list)                 # list of cloudinary URLs
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship 
    
    village = relationship("Village" , back_populates="projects")
    
    