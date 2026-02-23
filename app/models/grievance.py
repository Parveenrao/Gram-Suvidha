from sqlalchemy import Column , String , DateTime , ForeignKey , Enum , Float , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class GrievanceStatusEnum(String , enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"
    
 
class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(Integer , primary_key=True , index=True)
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    citizen_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    title = Column(String , nullable=False)
    description  = Column(String , nullable=False)
    category = Column(String , nullable=False)       #eg. road , water etc
    status = Column(Enum(GrievanceStatusEnum) , default = GrievanceStatusEnum.open)
    sarpanch_reply = Column(String , nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True) 
    
    
    # Relationship
    village = relationship("Village" , back_populates='grievances')
    
    citizens = relationship("User" , back_populates="grievances")