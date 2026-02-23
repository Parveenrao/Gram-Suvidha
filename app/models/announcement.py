from sqlalchemy import Column , String , Enum , DateTime , ForeignKey , Integer , Float , JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AnnouncementTypeEnum(str , enum.Enum):
    notice  = "notice"
    scheme =   "scheme"
    meeting =  "meeting"
    alert  =   "alert"
    general = "general"
    


class Announcement(Base):
    __tablename__ = 'announcements'
    
    id = Column(Integer , primary_key=True , index=True)
    village_id = Column(Integer , ForeignKey("villages.id") , nullable=False)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    type = Column(Enum(AnnouncementTypeEnum) , default=AnnouncementTypeEnum.general)
    published_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship 
    
    village = relationship("Village", back_populates="announcements")
    published_by_user = relationship("User", back_populates="announcements")
        