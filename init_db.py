#!/usr/bin/env python3
"""
Database initialization script for Mini Order Management Service
Creates tables and initial admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.models import Base, User
from app.core.security import hash_password
from app.core.config import settings

def init_db():
    """Initialize database with tables and admin user"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("Creating admin user...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hash_password("Admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: Admin123")
        else:
            print("Admin user already exists")
            
        print("Database initialization completed!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
