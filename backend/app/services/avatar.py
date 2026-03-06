"""Sign Language Avatar Service"""
import logging
from typing import Optional, List
from app.services.sign_language_converter import SignLanguageConverter

logger = logging.getLogger(__name__)

# Pre-defined ASL dictionary with common words
ASL_DICTIONARY = {
    # Greetings
    "hello": "asl_hello.mp4",
    "goodbye": "asl_goodbye.mp4",
    
    # Politeness
    "thank": "asl_thank.mp4",
    "please": "asl_please.mp4",
    "sorry": "asl_sorry.mp4",
    
    # Actions
    "help": "asl_help.mp4",
    "submit": "asl_submit.mp4",
    "send": "asl_send.mp4",
    "give": "asl_give.mp4",
    "take": "asl_take.mp4",
    "make": "asl_make.mp4",
    "see": "asl_see.mp4",
    "look": "asl_look.mp4",
    "hear": "asl_hear.mp4",
    "listen": "asl_listen.mp4",
    "read": "asl_read.mp4",
    "write": "asl_write.mp4",
    "type": "asl_type.mp4",
    "click": "asl_click.mp4",
    "find": "asl_find.mp4",
    "use": "asl_use.mp4",
    "work": "asl_work.mp4",
    "do": "asl_do.mp4",
    
    # Questions
    "what": "asl_what.mp4",
    "how": "asl_how.mp4",
    "when": "asl_when.mp4",
    "where": "asl_where.mp4",
    "why": "asl_why.mp4",
    "who": "asl_who.mp4",
    "whom": "asl_whom.mp4",
    "which": "asl_which.mp4",
    
    # Affirmations
    "yes": "asl_yes.mp4",
    "no": "asl_no.mp4",
    
    # Emotions
    "love": "asl_love.mp4",
    "happy": "asl_happy.mp4",
    "sad": "asl_sad.mp4",
    "feel": "asl_feel.mp4",
    
    # Objects & Things
    "form": "asl_form.mp4",
    "person": "asl_person.mp4",
    "water": "asl_water.mp4",
    "family": "asl_family.mp4",
    "friend": "asl_friend.mp4",
    "person": "asl_person.mp4",
    "task": "asl_task.mp4",
    "name": "asl_name.mp4",
    
    # Time
    "tomorrow": "asl_tomorrow.mp4",
    "today": "asl_today.mp4",
    "before": "asl_before.mp4",
    "after": "asl_after.mp4",
    "now": "asl_now.mp4",
    "soon": "asl_soon.mp4",
    "later": "asl_later.mp4",
    
    # Mental/Knowledge
    "understand": "asl_understand.mp4",
    "know": "asl_know.mp4",
    "think": "asl_think.mp4",
    
    # Needs/Desires
    "need": "asl_need.mp4",
    "want": "asl_want.mp4",
    
    # Quality
    "good": "asl_good.mp4",
    "bad": "asl_bad.mp4",
    "time": "asl_time.mp4",
    "right": "asl_right.mp4",
    "wrong": "asl_wrong.mp4",
    
    # Common pronouns (for better coverage)
    "i": "asl_i.mp4",
    "me": "asl_me.mp4",
    "you": "asl_you.mp4",
    "your": "asl_your.mp4",
    "he": "asl_he.mp4",
    "she": "asl_she.mp4",
    "it": "asl_it.mp4",
    "we": "asl_we.mp4",
    "they": "asl_they.mp4",
    
    # Common words to reduce fingerspelling
    "and": "asl_and.mp4",
    "or": "asl_or.mp4",
    "not": "asl_not.mp4",
    "this": "asl_this.mp4",
    "that": "asl_that.mp4",
    "these": "asl_these.mp4",
    "those": "asl_those.mp4",
    "all": "asl_all.mp4",
    "each": "asl_each.mp4",
    "one": "asl_one.mp4",
    "two": "asl_two.mp4",
    "three": "asl_three.mp4",
    "four": "asl_four.mp4",
    "five": "asl_five.mp4",
    "more": "asl_more.mp4",
    "less": "asl_less.mp4",
    "with": "asl_with.mp4",
    "for": "asl_for.mp4",
}


class SignLanguageAvatarService:
    """
    Service for generating sign language avatar animations
    Converts text to sign language animations for deaf/hard of hearing users
    """

    @staticmethod
    def text_to_sign_animation(text: str) -> dict:
        """
        Convert text to sign language animation instructions
        
        Args:
            text: Text to convert to sign language
            
        Returns:
            Dict with animation data and metadata
        """
        # Convert English to ASL grammar
        asl_words = SignLanguageConverter.convert_to_asl(text)
        
        # Get metadata about the conversion
        asl_metadata = SignLanguageConverter.get_asl_metadata(asl_words)
        
        animations = []
        unrecognized = []
        
        for word in asl_words:
            # Clean word of punctuation
            clean_word = word.strip(".,!?;:").lower()
            
            # Look up in ASL dictionary
            if clean_word in ASL_DICTIONARY:
                animations.append({
                    "word": word,
                    "asl_word": word,
                    "video": ASL_DICTIONARY[clean_word],
                    "duration": 1500,  # ms
                    "recognized": True
                })
            else:
                # Attempt to spell out word (fingerspelling)
                animations.append({
                    "word": word,
                    "asl_word": word,
                    "letters": list(clean_word.upper()),
                    "type": "fingerspell",
                    "duration": len(clean_word) * 200,  # 200ms per letter
                    "recognized": False
                })
                unrecognized.append(clean_word)
        
        return {
            "text": text,
            "asl_words": asl_words,
            "asl_sentence": " ".join(asl_words),
            "animations": animations,
            "total_duration_ms": sum(a.get("duration", 0) for a in animations),
            "unrecognized_words": unrecognized,
            "avatar_style": "3d",  # Could be "2d", "3d", "video"
            "grammar_metadata": asl_metadata,
        }

    @staticmethod
    def get_sign_language_variants() -> dict:
        """
        Get available sign language variants
        
        Returns:
            Dict of available sign language options
        """
        return {
            "ASL": "American Sign Language",
            "BSL": "British Sign Language",
            "DSL": "Danish Sign Language",
            "FSL": "French Sign Language",
            "DGS": "German Sign Language",
            "LSF": "French Sign Language",
            "JSL": "Japanese Sign Language",
            "CSL": "Chinese Sign Language",
        }

    @staticmethod
    def split_text_for_avatar(text: str, words_per_segment: int = 5) -> List[dict]:
        """
        Split text into segments for avatar animation
        
        Args:
            text: Text to split
            words_per_segment: Number of words per animation segment
            
        Returns:
            List of animation segments
        """
        words = text.split()
        segments = []
        
        for i in range(0, len(words), words_per_segment):
            segment_words = words[i:i + words_per_segment]
            segment_text = " ".join(segment_words)
            
            animation = SignLanguageAvatarService.text_to_sign_animation(segment_text)
            animation["segment_index"] = len(segments)
            segments.append(animation)
        
        return segments

    @staticmethod
    def generate_avatar_metadata(text: str) -> dict:
        """
        Generate metadata for avatar rendering
        
        Args:
            text: Text for avatar to sign
            
        Returns:
            Metadata for frontend avatar component
        """
        animation_data = SignLanguageAvatarService.text_to_sign_animation(text)
        
        return {
            "text": text,
            "word_count": len(text.split()),
            "recognized_words": sum(1 for a in animation_data["animations"] if a["recognized"]),
            "unrecognized_words": animation_data["unrecognized_words"],
            "total_duration_seconds": animation_data["total_duration_ms"] / 1000,
            "animation_data": animation_data,
            "avatar_speed": "normal",  # Could be "slow", "normal", "fast"
        }
