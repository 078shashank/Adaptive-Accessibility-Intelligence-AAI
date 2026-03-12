"""Tests for Avatar Service and Routes"""
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestAvatarService:
    """Test Sign Language Avatar Service"""

    def test_text_to_sign_animation(self):
        """Test text to sign animation conversion"""
        from app.services.avatar import SignLanguageAvatarService

        result = SignLanguageAvatarService.text_to_sign_animation("hello world")
        
        assert result["text"] == "hello world"
        assert "animations" in result
        assert len(result["animations"]) == 2
        assert result["total_duration_ms"] > 0

    def test_split_text_for_avatar(self):
        """Test text splitting for sequential animation"""
        from app.services.avatar import SignLanguageAvatarService

        long_text = "hello world this is a test of the sign language avatar"
        segments = SignLanguageAvatarService.split_text_for_avatar(long_text, words_per_segment=2)
        
        assert len(segments) > 0
        assert all("segment_index" in seg for seg in segments)

    def test_get_sign_language_variants(self):
        """Test getting available sign language variants"""
        from app.services.avatar import SignLanguageAvatarService

        variants = SignLanguageAvatarService.get_sign_language_variants()
        
        assert "ASL" in variants
        assert "BSL" in variants
        assert len(variants) > 0


@pytest.mark.asyncio
class TestAvatarRoutes:
    """Test Avatar API Routes"""

    async def test_generate_sign_language_unauthorized(self):
        """Test generating sign language without authentication"""
        response = client.post(
            "/api/v1/avatar/sign",
            json={"text": "hello world"}
        )
        
        assert response.status_code == 403

    async def test_generate_sign_language(self, token_helper):
        """Test generating sign language animation"""
        token = token_helper["token"]
        
        response = client.post(
            "/api/v1/avatar/sign",
            json={"text": "hello world"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "avatar_data" in data

    async def test_generate_sign_language_empty_text(self, token_helper):
        """Test generating sign language with empty text"""
        token = token_helper["token"]
        
        response = client.post(
            "/api/v1/avatar/sign",
            json={"text": ""},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400

    async def test_get_sign_languages(self, token_helper):
        """Test getting available sign languages"""
        token = token_helper["token"]
        
        response = client.get(
            "/api/v1/avatar/languages",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "languages" in data
        assert "current" in data

    async def test_segment_for_avatar(self, token_helper):
        """Test segmenting text for avatar animation"""
        token = token_helper["token"]
        
        response = client.post(
            "/api/v1/avatar/segment",
            json={"text": "hello world this is a test sentence"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "segments" in data
        assert "total_segments" in data
        assert len(data["segments"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
