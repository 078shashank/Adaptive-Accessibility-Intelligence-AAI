"""Speech Processing Service (TTS/STT)"""
import logging


logger = logging.getLogger(__name__)


class SpeechService:
    """
    Speech service wrapper for TTS/STT
    Uses browser Web Speech API on frontend
    Backend provides optional TTS endpoint
    """

    @staticmethod
    def prepare_text_for_speech(text: str, max_length: int = 500) -> str:
        """
        Prepare text for speech synthesis

        Args:
            text: Text to prepare
            max_length: Maximum length for a single speech utterance

        Returns:
            Prepared text for TTS
        """
        # Remove special characters that don't work well with TTS
        text = text.replace("&", "and")
        text = text.replace("@", "at")
        text = text.replace("#", "number")
        text = text.replace("_", " ")

        # Limit text length if needed
        if len(text) > max_length:
            # Find sentence boundary near max_length
            sentences = text.split(". ")
            result = ""
            for sentence in sentences:
                if len(result) + len(sentence) < max_length:
                    result += sentence + ". "
                else:
                    break
            return result if result else text[:max_length]

        return text

    @staticmethod
    def get_supported_languages() -> list:
        """
        Get list of supported languages for speech

        Returns:
            List of language codes
        """
        return [
            "en-US",  # English (US)
            "en-GB",  # English (UK)
            "es-ES",  # Spanish
            "fr-FR",  # French
            "de-DE",  # German
            "it-IT",  # Italian
            "pt-BR",  # Portuguese (Brazil)
            "ja-JP",  # Japanese
            "zh-CN",  # Chinese (Simplified)
            "ko-KR",  # Korean
        ]

    @staticmethod
    def validate_speech_rate(rate: float) -> float:
        """
        Validate and normalize speech rate

        Args:
            rate: Speech rate (0.5 to 2.0)

        Returns:
            Normalized speech rate
        """
        if rate < 0.5:
            return 0.5
        if rate > 2.0:
            return 2.0
        return rate

    @staticmethod
    def split_text_for_tts(text: str, max_utterance_length: int = 500) -> list:
        """
        Split long text into smaller utterances for TTS

        Args:
            text: Text to split
            max_utterance_length: Maximum characters per utterance

        Returns:
            List of text chunks
        """
        if len(text) <= max_utterance_length:
            return [text]

        chunks = []
        sentences = text.split(". ")
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_utterance_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]
