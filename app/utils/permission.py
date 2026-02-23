from fastapi import HTTPException, status , Depends
from app.models.user import RoleEnum
from app.utils.auth import get_current_user


def require_roles(*roles : RoleEnum):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Access denied. Required roles: {[r.value for r in roles]}")
        
        return current_user
    return checker