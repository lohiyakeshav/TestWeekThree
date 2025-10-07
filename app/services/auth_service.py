from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import verify_password_hash, create_access_token, verify_token, validate_password
from app.core.logger import log_action
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    @log_action("register_user")
    def register_user(self, user: UserCreate):
        if not validate_password(user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters with uppercase, lowercase, digit, and special character"
            )
        
        existing_user = self.user_repo.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        return self.user_repo.create_user(user)
    
    @log_action("authenticate_user")
    def authenticate_user(self, user_login: UserLogin):
        user = self.user_repo.get_user_by_username(user_login.username)
        if not user or not verify_password_hash(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id, "role": user.role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            }
        }
    
    @log_action("get_current_user")
    def get_current_user(self, token: str):
        payload = verify_token(token)
        user = self.user_repo.get_user_by_id(payload["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
