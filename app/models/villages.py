from sqlalchemy import Column  , Integer , String , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Village(Base):
    __tablename__ = "villages"
    
    id = Column(Integer , primary_key=True , index=True)
    name  = Column(String , nullable=False)
    district = Column(String , nullable=False)
    state = Column(String , nullable=False)
    pincode = Column(Integer , nullable=False)
    
    created_at = Column(DateTime(timezone=True) , server_default=func.now())
    
    # Relationship 
    
    users = relationship("User" , back_populates="village" , cascade="all, delete-orphan")
    budgets = relationship("Budget" , back_populates="village" , cascade="all, delete-orphan")
    projects = relationship("Project" , back_populates="village" , cascade="all, delete-orphan")
    announcements = relationship("Announcement" , back_populates="village" , cascade="all, delete-orphan")
    grievances = relationship("Grievance", back_populates="village" , cascade="all, delete-orphan")
    documents = relationship("Document" , back_populates="village" , cascade="all, delete-orphan")
    
    