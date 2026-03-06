"""Database Optimization - Indexing and Query Optimization"""
from sqlalchemy import Index, text
from sqlalchemy.dialects import sqlite
from app.database import Base, engine
from app.models import User, AccessibilityProfile, TextSimplification
import logging

logger = logging.getLogger(__name__)


def add_database_indexes():
    """
    Add indexes to improve query performance
    Should be called after database initialization
    """
    with engine.begin() as connection:
        # Index for user email lookup (authentication)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)
        """))
        logger.info("✓ Created index on users.email")
        
        # Index for accessibility profile user_id (foreign key)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_accessibility_profiles_user_id 
            ON accessibility_profiles(user_id)
        """))
        logger.info("✓ Created index on accessibility_profiles.user_id")
        
        # Index for text simplification user_id (foreign key)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_text_simplifications_user_id 
            ON text_simplifications(user_id)
        """))
        logger.info("✓ Created index on text_simplifications.user_id")
        
        # Index for text simplification caching (original_text + reading_level)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_text_simplifications_cache 
            ON text_simplifications(original_text, reading_level)
        """))
        logger.info("✓ Created index on text_simplifications cache lookup")
        
        # Index for timestamp-based queries (audit logs)
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_text_simplifications_created_at 
            ON text_simplifications(created_at)
        """))
        logger.info("✓ Created index on text_simplifications.created_at")
        
        # Index for user active status
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_users_is_active 
            ON users(is_active)
        """))
        logger.info("✓ Created index on users.is_active")


def analyze_database():
    """
    Run ANALYZE to update query optimizer statistics
    Should be called periodically in production
    """
    with engine.begin() as connection:
        connection.execute(text("ANALYZE"))
        logger.info("✓ Database statistics updated")


def vacuum_database():
    """
    Run VACUUM to reclaim free space
    Should be called after large deletions
    """
    with engine.begin() as connection:
        connection.execute(text("VACUUM"))
        logger.info("✓ Database optimized (VACUUM completed)")


def get_database_stats():
    """Get database statistics for monitoring"""
    with engine.begin() as connection:
        # Count tables
        tables_result = connection.execute(text("""
            SELECT COUNT(*) FROM sqlite_master WHERE type='table'
        """))
        table_count = tables_result.scalar()
        
        # Count indexes
        indexes_result = connection.execute(text("""
            SELECT COUNT(*) FROM sqlite_master WHERE type='index'
        """))
        index_count = indexes_result.scalar()
        
        # Count rows per table
        users_result = connection.execute(text("SELECT COUNT(*) FROM users"))
        user_count = users_result.scalar()
        
        profiles_result = connection.execute(text(
            "SELECT COUNT(*) FROM accessibility_profiles"
        ))
        profile_count = profiles_result.scalar()
        
        simplifications_result = connection.execute(text(
            "SELECT COUNT(*) FROM text_simplifications"
        ))
        simplification_count = simplifications_result.scalar()
        
        return {
            "tables": table_count,
            "indexes": index_count,
            "users": user_count,
            "accessibility_profiles": profile_count,
            "text_simplifications": simplification_count
        }


def optimize_query_text_simplification(text: str, reading_level: str):
    """
    Optimized query for checking cached simplified text
    Uses indexed columns for fast lookup
    """
    from app.models import TextSimplification
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # This query uses the ix_text_simplifications_cache index
        result = db.query(TextSimplification).filter(
            TextSimplification.original_text == text,
            TextSimplification.reading_level == reading_level
        ).first()
        return result
    finally:
        db.close()


def get_user_profile_optimized(user_id: int):
    """
    Optimized query for getting user accessibility profile
    Uses indexed foreign key
    """
    from app.models import AccessibilityProfile
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # This query uses the ix_accessibility_profiles_user_id index
        result = db.query(AccessibilityProfile).filter(
            AccessibilityProfile.user_id == user_id
        ).first()
        return result
    finally:
        db.close()


# Connection pooling configuration for production
def get_optimized_engine():
    """
    Get database engine with optimized settings for production
    """
    from sqlalchemy import create_engine, event
    
    # Override if needed for production database (PostgreSQL, etc.)
    db_url = "sqlite:///./aai.db"
    
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,   # Recycle connections after 1 hour
    )
    
    # Enable query logging for debugging
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        """Log all SQL queries"""
        if "SELECT" in statement or "UPDATE" in statement:
            logger.debug(f"💾 SQL: {statement[:100]}...")
    
    return engine


if __name__ == "__main__":
    # Run optimizations
    logger.info("Starting database optimization...")
    add_database_indexes()
    analyze_database()
    stats = get_database_stats()
    logger.info(f"Database stats: {stats}")
    logger.info("✓ Database optimization complete")
