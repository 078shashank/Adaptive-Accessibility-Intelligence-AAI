import sys
import os
sys.path.insert(0, os.getcwd())

from app.database import SessionLocal
from app.models import User, AccessibilityProfile
from app.services.auth import get_password_hash

db = SessionLocal()

try:
    # Check if demo user exists
    demo_user = db.query(User).filter(User.email == 'demo@aai.com').first()
    if demo_user:
        print('Demo user already exists')
    else:
        # Create demo user
        user = User(
            email='demo@aai.com',
            full_name='Demo User',
            hashed_password=get_password_hash('demo123456'),
            is_active=True
        )
        db.add(user)
        db.flush()
        
        # Create profile
        profile = AccessibilityProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        print('Demo user created: demo@aai.com / demo123456')
finally:
    db.close()
