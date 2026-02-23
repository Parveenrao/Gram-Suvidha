from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.document import Document, DocumentTypeEnum
from app.models.user import RoleEnum
from app.schema.document import DocumentResponse , DocumentUpdate
from app.utils.auth import get_current_user
from app.utils.file_uploads import save_locally_documents


router = APIRouter()

#------------------------------- Public Endpoints -------------------------

# Get documents 

@router.get("/" , response_model=List[DocumentResponse])

def get_all_documents(village_id : int  ,  db : Session = Depends(get_db)):
    
    """
    Get all documents of a village.
    Public — any citizen can view and download.
    Example: /api/documents/?village_id=1
    """
    
    documents = db.query(Document).filter(Document.village_id == village_id).order_by(Document.created_at.desc()).all()
    
    return documents

# Get document by types 

@router.get("/type/{doc_type}" , response_model=List[DocumentResponse])

def get_document_by_type(viilage_id : int , doc_type : DocumentTypeEnum , db: Session = Depends(get_db)):
    
    """
    Get documents filtered by type.
    Example: /api/documents/type/budget_report?village_id=1
    Types """
    
    documents = db.query(Document).filter(Document.village_id == viilage_id , Document.type == doc_type).order_by(
                                             Document.created_at.desc()).all()
    
    return documents

# Get documents by id 

@router.get("/{document_id}" , response_model=DocumentResponse)

def get_document(document_id : int , db:Session = Depends(get_db)):
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise FileNotFoundError("Document not found")
    
    return document



#------------------------------------------- Admin endpoints------------------------------



# upload document 




@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document_file(
    title: str = Form(...),
    doc_type: DocumentTypeEnum = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in [RoleEnum.sarpanch, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only Sarpanch can upload documents")

    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "image/jpeg",
        "image/png"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    await file.seek(0)

   
    file_path = save_locally_documents(file)

    document = Document(
        village_id=current_user.village_id,
        title=title,
        file_url=file_path,   # store local path
        type=doc_type,
        uploaded_by=current_user.id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

# Update details of document 

@router.patch("/{document_id}" , response_model=DocumentResponse)

def update_document(document_id : int , data : DocumentUpdate, db : Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # check role 
    
    if current_user.role not in [RoleEnum.sarpanch, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only Sarpanch can update documents")
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.village_id == current_user.village_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key , value in update_data.items():
        setattr(Document , key , value)
        
    db.commit()
    db.refresh(document)

    return document   


# Delete document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    SARPANCH / ADMIN ONLY — Delete a document.
    Deletes from Cloudinary AND from DB.
    """
    if current_user.role not in [RoleEnum.sarpanch, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only Sarpanch can delete documents")

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.village_id == current_user.village_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

   
    # Delete from DB
    db.delete(document)
    db.commit()
    return {"message": f"Document '{document.title}' deleted successfully ✅"} 

    
    