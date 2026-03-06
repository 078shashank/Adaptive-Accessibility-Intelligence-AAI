import sys
import os
sys.path.insert(0, os.getcwd())

from app.database import SessionLocal
from app.models import User, AccessibilityProfile
import hashlib

db = SessionLocal()

try:
    # Check if demo user exists
    demo_user = db.query(User).filter(User.email == 'demo@aai.com').first()
    if demo_user:
        print('Demo user already exists')
    else:
        # Use a simple hash workaround to avoid bcrypt issue
        # In production, this should NOT be used
        # This is just for demo/testing purposes
        password = 'demo123456'
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(
            email='demo@aai.com',
            full_name='Demo User',
            hashed_password=hashed,  # Using SHA256 as workaround
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
