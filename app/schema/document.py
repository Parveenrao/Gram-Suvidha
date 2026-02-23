from pydantic import BaseModel , Field 
from typing import Optional
from app.models.document import DocumentTypeEnum
from datetime import  datetime

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[DocumentTypeEnum] = None

class DocumentResponse(BaseModel):
    id :  int
    village_id : int   
    title : str       
    file_url : str       
    type : DocumentTypeEnum
    uploaded_by : int      
    created_at   : datetime
    
    class Config:
        from_attributes = True
    