from pydantic import BaseModel , EmailStr , Field , field_validator , model_validator
from typing import Optional
from app.models.user import RoleEnum



class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class UpdateMe(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# When registering a new user

class UserCreate(BaseModel):
    name : str
    phone : str
    email : Optional[EmailStr] = None  # NOt required
    password : str
    confirm_password: str 
    ward_number : Optional[int] = None
    village_id : int    # Required
    is_active : bool
    
    
     # Password strength
    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    # Confirm password check
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    

# Only admin can use this — can set any role

class AdminUserCreate(BaseModel):
  
    name: str
    phone: str
    email: Optional[EmailStr] = None
    password: str
    role: RoleEnum                      # admin sets the role
    ward_number: Optional[int] = None   # required if ward_member
    village_id: int    
    
    
# Admin updates role of existing user  
    
class UserRoleUpdate(BaseModel):
   
    role: RoleEnum
    ward_number: Optional[int] = None   # required if ward_member    
    
# User Login(Only Phone and Password)

from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    phone: str = Field(
        ...,
        min_length=10,
        max_length=10,
        pattern=r"^\d{10}$",
        description="10 digit phone number"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Password with upper and lowercase letters"
    )

    
# What we send back to user 

class UserResponse(BaseModel):
    id : int
    name : str
    phone : str
    role : RoleEnum
    ward_number : Optional[int] = None
    village_id : int
    is_active : bool
    
    
    class Config:
        from_attributes = True     # allows reading from SQLAlchemy model
        
        
# what we send after successfull login 

class Token(BaseModel):
    access_token : str
    token_type : str
    user : UserResponse        