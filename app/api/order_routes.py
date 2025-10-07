from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.order_service import OrderService
from app.services.auth_service import AuthService
from app.schemas.order import OrderCreate, OrderResponse, OrderListResponse
from app.core.logger import log_action

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)

@router.post("/create", response_model=OrderResponse)
@log_action("create_order")
def create_order(order: OrderCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.create_order(order, current_user.id, current_user.email, background_tasks)

@router.get("/", response_model=OrderListResponse)
@log_action("get_orders")
def get_orders(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    order_service = OrderService(db)
    
    if current_user.role == "admin":
        orders = order_service.get_all_orders()
    else:
        orders = order_service.get_user_orders(current_user.id)
    
    return OrderListResponse(orders=orders)
