"""Text Simplification Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User, TextSimplification
from app.schemas import TextSimplifyRequest, TextSimplifyResponse
from app.services.text_adapter import simplify_text as npl_simplify_text
from app.dependencies import get_current_user_optional

router = APIRouter(prefix="/text", tags=["text"])


@router.post("/simplify", response_model=TextSimplifyResponse)
async def simplify_text(
    request: TextSimplifyRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Simplify complex text using NLP
    
    Args:
        request: TextSimplifyRequest with text and reading level
        current_user: Authenticated user
        db: Database session
        
    Returns:
        TextSimplifyResponse with simplified text
        
    Raises:
        HTTPException: If text is too short or long
    """
    # Validate text length
    if len(request.text) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text must be at least 10 characters"
        )
    
    if len(request.text) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text must be less than 5000 characters"
        )
    
    # Call NLP service to simplify
    try:
        simplified = npl_simplify_text(request.text, request.reading_level)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error simplifying text: {str(e)}"
        )
    
    # Save to database for caching (only if user is authenticated)
    if current_user:
        try:
            cache_entry = TextSimplification(
                user_id=current_user.id,
                original_text=request.text,
                simplified_text=simplified,
                reading_level=request.reading_level
            )
            db.add(cache_entry)
            db.commit()
        except Exception as db_error:
            # Log but don't fail if caching fails
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to cache simplification: {db_error}")
            db.rollback()
    
    return {
        "original_text": request.text,
        "simplified_text": simplified,
        "reading_level": request.reading_level
    }
