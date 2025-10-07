from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderCreate(BaseModel):
    success: bool

class OrderResponse(BaseModel):
    id: int
    user_id: int
    success: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
