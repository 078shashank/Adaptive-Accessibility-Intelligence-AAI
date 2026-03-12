"""Tests for Speech Service"""
import pytest
from app.services.speech import SpeechService


class TestSpeechService:
    """Test Speech Processing Service"""

    def test_prepare_text_for_speech(self):
        """Test text preparation for speech synthesis"""
        text = "Hello @ world & friends"
        result = SpeechService.prepare_text_for_speech(text)

        assert "and" in result
        assert "at" in result
        assert "@" not in result
        assert "&" not in result

    def test_prepare_text_long(self):
        """Test text truncation for long texts"""
        long_text = "a " * 600
        result = SpeechService.prepare_text_for_speech(long_text, max_length=500)

        assert len(result) <= 510  # Allow some buffer for sentence boundaries

    def test_validate_speech_rate(self):
        """Test speech rate validation"""
        assert SpeechService.validate_speech_rate(0.5) == 0.5
        assert SpeechService.validate_speech_rate(1.0) == 1.0
        assert SpeechService.validate_speech_rate(2.0) == 2.0
        assert SpeechService.validate_speech_rate(0.1) == 0.5  # Minimum
        assert SpeechService.validate_speech_rate(3.0) == 2.0  # Maximum

    def test_split_text_for_tts(self):
        """Test text splitting for TTS"""
        text = "Hello world. This is a test. Another sentence. Final sentence."
        chunks = SpeechService.split_text_for_tts(text, max_utterance_length=30)
        
        assert len(chunks) > 0
        assert all(len(chunk) <= 40 for chunk in chunks)  # Allow some buffer

    def test_split_text_short(self):
        """Test splitting short text"""
        text = "Hello"
        chunks = SpeechService.split_text_for_tts(text)
        
        assert len(chunks) == 1
        assert chunks[0] == "Hello"

    def test_get_supported_languages(self):
        """Test getting supported languages"""
        languages = SpeechService.get_supported_languages()
        
        assert len(languages) > 0
        assert "en-US" in languages
        assert "es-ES" in languages


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
