"""
ASL Sign Language Grammar Converter
Converts English text to ASL (American Sign Language) word order and grammar
"""

import re
from typing import List, Dict


class SignLanguageConverter:
    """
    Converts English sentences to ASL grammar structure.
    ASL is topic-prominent and uses different grammar than English.
    
    Example:
    English: "Please submit the form before tomorrow."
    ASL: "TOMORROW FORM SUBMIT PLEASE"
    """

    # Common English words to filter out (many are implied in ASL)
    REMOVE_ARTICLES = {'a', 'an', 'the'}
    REMOVE_PREPOSITIONS = {'in', 'on', 'at', 'by', 'with', 'for'}
    REMOVE_AUXILIARY_VERBS = {'is', 'am', 'are', 'was', 'were', 'be', 'being', 'been'}

    # Question words (typically move to front in ASL)
    QUESTION_WORDS = {'how', 'what', 'when', 'where', 'why', 'who', 'whom', 'which'}

    # Time expressions (typically move to front in ASL - Topic position)
    TIME_WORDS = {
        'tomorrow', 'today', 'yesterday', 'now', 'then', 'soon', 'later',
        'morning', 'afternoon', 'evening', 'night', 'day', 'week', 'month', 'year',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    }

    # Action verbs (usually come before objects in ASL)
    ACTION_VERBS = {
        'submit', 'send', 'give', 'take', 'make', 'help', 'want', 'need',
        'see', 'look', 'hear', 'listen', 'read', 'write', 'type', 'click',
        'understand', 'know', 'think', 'feel', 'find', 'use', 'work', 'do'
    }

    @staticmethod
    def convert_to_asl(english_text: str) -> List[str]:
        """
        Convert English text to ASL word order.
        Returns list of signs to display.
        
        Args:
            english_text: English sentence
            
        Returns:
            List of ASL words in correct order
        """
        # Normalize text
        text = english_text.lower().strip()

        # Remove punctuation but keep sentence markers
        is_question = text.endswith('?')
        text = re.sub(r'[^\w\s?]', '', text)

        # Split into words
        words = text.split()
        
        # Remove filtered words
        filtered_words = [w for w in words if w not in SignLanguageConverter.REMOVE_ARTICLES
                          and w not in SignLanguageConverter.REMOVE_AUXILIARY_VERBS]

        # Reorganize to ASL order
        asl_words = SignLanguageConverter._reorganize_to_asl(filtered_words, is_question)
        
        return asl_words

    @staticmethod
    def _reorganize_to_asl(words: List[str], is_question: bool) -> List[str]:
        """
        Reorganize words to ASL grammar structure.

        ASL Structure:
        1. Topic (time, location, or main subject)
        2. Subject
        3. Verb
        4. Object
        5. Modifiers
        6. Question marker (if question)
        """
        if not words:
            return []

        # Categorize words
        time_words = [w for w in words if w in SignLanguageConverter.TIME_WORDS]
        question_words = [w for w in words if w in SignLanguageConverter.QUESTION_WORDS]
        action_words = [w for w in words if w in SignLanguageConverter.ACTION_VERBS]

        remaining = [w for w in words 
                    if w not in time_words 
                    and w not in question_words
                    and w not in action_words]
        
        # Build ASL order: Time/Topic → Remaining → Actions → Questions
        asl_order = time_words + remaining + action_words + question_words

        # Capitalize all words (ASL notation)
        asl_order = [w.upper() for w in asl_order]
        
        return asl_order

    @staticmethod
    def get_asl_metadata(asl_words: List[str]) -> Dict:
        """
        Get metadata about the ASL phrase.

        Returns:
            Dictionary with phrase info
        """
        return {
            'word_count': len(asl_words),
            'words': asl_words,
            'is_question': any(w in {'WHAT', 'WHO', 'WHERE', 'WHEN', 'WHY', 'HOW'} for w in asl_words),
            'has_actions': any(w in {v.upper() for v in SignLanguageConverter.ACTION_VERBS} for w in asl_words),
            'has_time': any(w in {t.upper() for t in SignLanguageConverter.TIME_WORDS} for w in asl_words),
        }


def simplify_text_to_signs(english_text: str) -> Dict:
    """
    Convert English text to simplified ASL signs.

    Example:
    Input: "Please submit the form before tomorrow"
    Output: {
        'original': 'Please submit the form before tomorrow',
        'asl_words': ['TOMORROW', 'FORM', 'SUBMIT', 'PLEASE'],
        'metadata': {...}
    }
    """
    asl_words = SignLanguageConverter.convert_to_asl(english_text)
    metadata = SignLanguageConverter.get_asl_metadata(asl_words)

    return {
        'original': english_text,
        'asl_words': asl_words,
        'asl_sentence': ' '.join(asl_words),
        'metadata': metadata
    }
