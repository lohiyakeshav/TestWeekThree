from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.core.logger import log_action

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=UserResponse)
@log_action("user_registration")
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_user(user)

@router.post("/login", response_model=Token)
@log_action("user_login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.authenticate_user(user_login)

@router.get("/me", response_model=UserResponse)
@log_action("get_user_info")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)
