from fastapi import HTTPException , Request
from fastapi.responses import JSONResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)                # is  a Python built-in variable that holds the current file's module path.
                                             # __name__ = "app.utils.exceptions"




#--------------------------------Custom Exception ------------------------

class AppException(HTTPException):
    def __init__(self, status_code :int , detail : str):
        super().__init__(status_code=status_code , detail=detail)
        
        
class NotFoundException(HTTPException):
    def __init__(self , detail : str = "Resource not found"):
        super().__init__(status_code=404 , detail=detail)

class UnauthorizeException(HTTPException):
    def __init__(self, detail : str = "Unauthorized"):
        super().__init__(status_code=401 , detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self,  detail : str = "Forbidden"):
        super().__init__(status_code = 403 , detail=detail)
        
class BadRequestException(HTTPException):
    def __init__(self , detail : str = "Bad Request"):
        super().__init__(status_code=400 , detail=detail)

class ConflictException(HTTPException):
    def __init__(self , detail : str = "Conflict"):
        super().__init__(status_code=409 , detail=detail)                                       
 



# ── Exception Handlers (register in main.py) ──────────────
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"{exc.status_code} | {request.method} {request.url} | {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail}
    )


# handle unexpected error

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error | {request.method} {request.url} | {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "Internal server error"}
    )