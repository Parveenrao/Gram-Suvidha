from fastapi import APIRouter , HTTPException , status , Depends 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User , RoleEnum
from app.models.villages import Village
from app.schema.user import UserCreate , UserLogin , UserResponse , AdminUserCreate , Token , UserRoleUpdate , PasswordUpdate , UpdateMe
from app.utils.auth import hash_password , get_current_user , verify_password , create_access_token
from app.utils.exception import ConflictException  , NotFoundException , UnauthorizeException , ForbiddenException ,  BadRequestException


router = APIRouter()


@router.post("/register" , response_model=UserResponse , status_code=201)

def register(user_data : UserCreate , db : Session = Depends(get_db)):
    # Anyone can register ---- always become citizen 
    # Role cannont be choose by user 
    
    # check phone_number already register 
    if db.query(User).filter(User.phone == user_data.phone).first():
        raise ConflictException("Phone number already registerd")
    
    # Check if email already registered
    if user_data.email:
        if db.query(User).filter(User.email == user_data.email).first():
            raise ConflictException("Email already registered")
        
    # Check if  village already registered
    vilage = db.query(Village).filter(Village.id == user_data.village_id).first()
    
    if not vilage:
        raise  NotFoundException("Village not found")
    
    hashed_password = hash_password(user_data.password)
    
    user = User(name = user_data.name,
                phone = user_data.phone,
                email = user_data.email,
                hashed_password = hashed_password,
                role = RoleEnum.citizen,
                ward_number = user_data.ward_number,
                village_id = user_data.village_id,
                is_active = True)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

    
#--------------------- Public Endpoints---------------------------------    
    
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.phone == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

#------------------- Logged-In Endpoints-----------------------

@router.get("/me" , response_model=UserResponse)

def get_me(current_user = Depends(get_current_user)):
    
    return current_user       # Get current logged in user


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UpdateMe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_fields = ["name", "email"]

    for key, value in data.dict(exclude_unset=True).items():
        if key in allowed_fields:
            setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/change-password")

def update_password(data : PasswordUpdate , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # change own password --> must provide old password first
    
    old_password = data.old_password
    new_password = data.new_password
    
    
    if not old_password and new_password:
        raise BadRequestException("Both Old and New password required")
    
    
    if not verify_password(old_password , current_user.hashed_password):
        raise BadRequestException("Old password is incorrect")
    
    if len(new_password) < 6:
        raise BadRequestException("New password must be at least 6 character")
    
    current_user.hashed_password = hash_password(new_password)
    
    db.commit()
    
    return {"message" : "Password change successfully"}


#----------------- Admin Only Endpoints-------------------------

@router.post("/admin/register-user" , response_model=UserResponse , status_code=201)

def admin_register_user(user_data : AdminUserCreate , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # ADMIN --> register sarpanch and ward members directly 
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can register privileged users")
    
    
    if db.query(User).filter(User.phone == user_data.phone).first():
        raise ConflictException("Phone number already registered")
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise ConflictException("Email already registered")
    
    village = db.query(Village).filter(User.village_id == user_data.village_id).first()
    
    if not village:
        raise NotFoundException("Village not found")
    
    if user_data.role in [RoleEnum.ward_citizen, RoleEnum.sarpanch] and not user_data.ward_number:
        raise BadRequestException("ward_number required for ward members and sarpanch")
    
    
    user = User(name = user_data.name,
                phone = user_data.phone,
                email = user_data.email,
                hashed_password = hash_password(user_data.password),
                role = user_data.role,
                ward_number = user_data.ward_number,
                village_id = user_data.village_id,
                is_active = True)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/admin/users" , response_model=List[UserResponse])

def get_all_users(db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # Admin only --> Get all user 
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can view all users")
    
    return db.query(User).all()


@router.get("/admin/users/{user_id}" , response_model= UserResponse)
    
def get_user(user_id : int , db:Session = Depends(get_db)  , current_user  = Depends(get_current_user)):
        if current_user.role != RoleEnum.admin:
            raise ForbiddenException("Only user can view user details")
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise NotFoundException("User not found")
        
        return user
    
    
# Update user role 

@router.patch("admin/users/{user_id}/role")

def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can update role")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")

    # Ward validation
    if data.role == RoleEnum.ward_citizen and data.ward_number is None:
        raise BadRequestException("Ward number required for ward citizen")

    user.role = data.role

    # Only update ward_number if explicitly provided
    if data.ward_number is not None:
        user.ward_number = data.ward_number

    # IMPORTANT: don't null ward unless DB allows it
    if data.role == RoleEnum.sarpanch:
        pass   # leave existing ward_number OR use special value

    db.commit()

    return {"message": f"Role updated to {data.role} for {user.name}"}
    
     
# Delete user 

@router.delete("/admin/users/{user_id}")

def delete_user(user_id : int , db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    
    # Admin ---> delete a user permanently 
    
    if current_user.role != RoleEnum.admin:
        raise ForbiddenException("Only Admin can delete users")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise NotFoundException('User not found')
    
    
    db.delete(user)
    db.commit()
    
    return {"message" : f"User {user.name} is deleted successfully "}     