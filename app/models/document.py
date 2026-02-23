from sqlalchemy import Column , String , DateTime , ForeignKey , Enum , Float , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class DocumentTypeEnum(String , enum.Enum):
    certificate = "certificate"
    notice = "notice"
    budget_report = "budget_report"
    meeting_minutes = "meeting_minutes"
    other  = "other"
    

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer , primary_key=True , index=True)
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    title = Column(String , nullable=False)
    file_url = Column(String , nullable=False)
    type = Column(Enum(DocumentTypeEnum), default=DocumentTypeEnum.other)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())    
    
    # Relationship 
    
    village = relationship("Village", back_populates="documents")