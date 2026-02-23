from sqlalchemy import Column , Integer , String , DateTime , Boolean , ForeignKey , Enum , Boolean 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum 
from app.database import Base


class RoleEnum(str , enum.Enum):
    admin = "admin"
    sarpanch = "sarpanch"
    ward_citizen = "ward_citizen"
    citizen = "citizen"
    


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key=True , index=True)
    name = Column(String , nullable=False) 
    phone = Column(String(15) , unique=True , nullable=False) 
    email = Column(String , unique=True , nullable=False)
    hashed_password = Column(String , nullable=False)
    role = Column(Enum(RoleEnum) , default=RoleEnum.citizen)
    ward_number = Column(Integer , nullable=False)            # for ward memebers
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    is_active = Column(Boolean , default=True)
    created_at = Column(DateTime(timezone=True) , server_default=func.now())  
    
    # Relationship 
    
    village = relationship("Village" , back_populates="users")
    grievances = relationship("Grievance" , back_populates="citizens")
    announcements = relationship("Announcement" , back_populates="published_by_user")
    