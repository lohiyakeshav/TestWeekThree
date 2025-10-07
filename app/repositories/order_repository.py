from sqlalchemy.orm import Session
from app.db.models import Order
from app.schemas.order import OrderCreate

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order: OrderCreate, user_id: int) -> Order:
        db_order = Order(
            user_id=user_id,
            success=order.success
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_user_orders(self, user_id: int) -> list[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()
    
    def get_all_orders(self) -> list[Order]:
        return self.db.query(Order).all()
