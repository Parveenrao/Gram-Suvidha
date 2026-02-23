import uuid
from pathlib import Path
from fastapi  import UploadFile
  
UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  


def save_locally_documents(file : UploadFile) -> str:
    
    ext = Path(file.filename).suffix         # extract the last part of file like parveen.xls (xls)
    
    filename = f"{uuid.uuid4()}{ext}"        # unique name to file so that not collide
    
    filepath = UPLOAD_DIR / filename
    
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return str(filepath)