from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.services.email_service import EmailService
from app.schemas.order import OrderCreate
from app.core.logger import log_action
from fastapi import HTTPException, status
from fastapi import BackgroundTasks

class OrderService:
    def __init__(self, db: Session):
        self.order_repo = OrderRepository(db)
    
    @log_action("create_order")
    def create_order(self, order: OrderCreate, user_id: int, user_email: str, background_tasks: BackgroundTasks):
        try:
            # Create order in database
            db_order = self.order_repo.create_order(order, user_id)
            
            # Schedule email notification in background; errors won't block request
            if order.success:
                background_tasks.add_task(EmailService.send_success_email, user_email)
            else:
                background_tasks.add_task(EmailService.send_failure_email, user_email)
            
            return db_order
        except Exception as e:
            # Rollback is handled by SQLAlchemy session
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Order creation failed: {str(e)}"
            )
    
    @log_action("get_user_orders")
    def get_user_orders(self, user_id: int):
        return self.order_repo.get_user_orders(user_id)
    
    @log_action("get_all_orders")
    def get_all_orders(self):
        return self.order_repo.get_all_orders()
