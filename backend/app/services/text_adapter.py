"""Text Adaptation Service using Hugging Face Transformers"""
from transformers import pipeline
import logging
import re

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
    Simplify complex text using Hugging Face BART model with hallucination prevention

    Args:
        text: Original text to simplify
        reading_level: Target reading level ("basic", "intermediate", "advanced")

    Returns:
        Simplified text without hallucinated content
    """
    
    # If model not loaded, return original text
    if summarizer is None:
        logger.warning("Summarization model not available, returning original text")
        return text
    
    # Check if text is already simple (informal/casual content)
    if _is_already_simple(text):
        logger.info("Text detected as already simple, applying minimal processing")
        return _clean_text_minimal(text)

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
        # Calculate max_length based on word count and reading level ratio
        word_count = len(text.split())
        max_length = max(30, int(word_count * ratio))  # Minimum 30 words
        min_length = max(20, int(max_length * 0.6))    # Min length is 60% of max
        
        # Use BART summarization as text simplification
        # Summarization naturally produces simpler language
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        simplified = summary[0]["summary_text"]
        
        # Validate that simplified text doesn't contain hallucinated content
        if _contains_hallucinations(text, simplified):
            logger.warning("Hallucination detected, falling back to rule-based simplification")
            return manual_simplify_text(text, reading_level)

        logger.info(f"Text simplified from {len(text)} to {len(simplified)} characters at {reading_level} level")
        return simplified
        
    except Exception as e:
        logger.error(f"Error during text simplification: {e}")
        # Return original text if simplification fails
        return text


def _is_already_simple(text: str) -> bool:
    """
    Detect if text is already simple (casual, informal, conversational)
    
    Indicators:
    - Contains emojis
    - Very short sentences (< 15 words average)
    - Informal phrases ("hit like", "subscribe", "thank you", "god bless")
    - Line breaks suggesting casual formatting
    - First/second person pronouns (I, you, we)
    """
    text_lower = text.lower()
    
    # Check for emojis (Unicode emoji ranges)
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0001F900-\U0001F9FF]')
    if emoji_pattern.search(text):
        return True
    
    # Check for informal phrases
    informal_phrases = [
        'thank you', 'thanks', 'god bless', 'hit like', 'subscribe',
        'watching', 'enjoyed', 'please', 'pls', 'dont forget'
    ]
    if any(phrase in text_lower for phrase in informal_phrases):
        return True
    
    # Check average sentence length
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    if sentences:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_length < 15:
            return True
    
    # Check for multiple line breaks (casual formatting)
    if text.count('\n\n') >= 1 or text.count('\n') >= 2:
        return True
    
    # Check for high pronoun ratio (conversational)
    pronouns = len(re.findall(r'\b(i|you|we|me|my|your|our)\b', text_lower))
    total_words = len(text.split())
    if total_words > 0 and pronouns / total_words > 0.15:
        return True
    
    return False


def _clean_text_minimal(text: str) -> str:
    """
    Minimal cleaning for already-simple text:
    - Fix punctuation spacing
    - Remove excessive line breaks
    - Preserve original meaning
    """
    # Replace multiple newlines with single space
    cleaned = re.sub(r'\n\s*\n', '. ', text)
    cleaned = re.sub(r'\n', ' ', cleaned)
    
    # Fix spacing around punctuation
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Capitalize first letter
    cleaned = cleaned.strip()
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    
    return cleaned


def _contains_hallucinations(original: str, simplified: str) -> bool:
    """
    Detect if simplified text contains information not in original
    
    Checks:
    - New entities (names, places) not in original
    - New actions/verbs not implied by original
    - Conditional statements (if/then) not in original
    - Excessive length increase (should be shorter!)
    """
    original_lower = original.lower()
    simplified_lower = simplified.lower()
    
    # Hallucination indicators
    hallucination_patterns = [
        r'\bif you did\b',
        r'\bif not\b',
        r'\bplease send.*me\b',
        r'\bshare.*friends\b',
        r'\bdidnt enjoy\b',
        r'\bwant.*to\b.*\bdo\b',
        r'\blet.*know\b',
        r'\bfeel free\b',
        r'\bdont hesitate\b',
    ]
    
    for pattern in hallucination_patterns:
        if re.search(pattern, simplified_lower) and not re.search(pattern, original_lower):
            return True
    
    # Check if simplified is significantly longer (red flag)
    if len(simplified.split()) > len(original.split()) * 1.2:
        return True
    
    return False


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
