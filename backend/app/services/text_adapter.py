"""Text Adaptation Service using Hugging Face Transformers"""
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Initialize summarization pipeline (acts as text simplification)
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    logger.info("Text summarization model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load summarization model: {e}")
    summarizer = None


def simplify_text(text: str, reading_level: str = "intermediate") -> str:
    """
    Simplify complex text using Hugging Face BART model

    Args:
        text: Original text to simplify
        reading_level: Target reading level ("basic", "intermediate", "advanced")

    Returns:
        Simplified text
    """
    
    # If model not loaded, return original text
    if summarizer is None:
        logger.warning("Summarization model not available, returning original text")
        return text

    # Determine summarization ratio based on reading level
    reading_level_config = {
        "basic": 0.35,      # Remove 65% of content
        "intermediate": 0.50,  # Remove 50% of content
        "advanced": 0.75    # Remove 25% of content
    }

    ratio = reading_level_config.get(reading_level, 0.50)

    # For short texts, return as-is
    if len(text.split()) < 20:
        return text
    
    try:
        # Use BART summarization as text simplification
        # Summarization naturally produces simpler language
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        simplified = summary[0]["summary_text"]

        logger.info(f"Text simplified from {len(text)} to {len(simplified)} characters")
        return simplified
        
    except Exception as e:
        logger.error(f"Error during text simplification: {e}")
        # Return original text if simplification fails
        return text


def manual_simplify_text(text: str, reading_level: str = "intermediate") -> str:
    """
    Fallback: Manual text simplification without ML (for testing/offline)

    Args:
        text: Original text
        reading_level: Target reading level

    Returns:
        Simplified text
    """
    # Simple rule-based simplification
    simplified = text

    # Remove complex punctuation
    simplified = simplified.replace("—", "-")
    simplified = simplified.replace("…", "...")

    # Remove parenthetical explanations for basic level
    if reading_level == "basic":
        import re
        simplified = re.sub(r'\([^)]*\)', '', simplified)
    
    # Keep sentences shorter for basic level
    if reading_level == "basic":
        sentences = simplified.split(". ")
        simplified = ". ".join([s[:80] for s in sentences])  # Limit sentence length

    return simplified
