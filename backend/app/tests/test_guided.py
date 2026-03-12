"""Tests for Guided Mode Service and Routes"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.guided_mode import GuidedModeService, GuidedStep

client = TestClient(app)


class TestGuidedModeService:
    """Test Guided Mode Service"""

    def test_get_step_instructions(self):
        """Test getting instructions for a step"""
        instructions = GuidedModeService.get_step_instructions(GuidedStep.WELCOME)

        assert instructions["title"] == "Welcome to Guided Mode"
        assert "description" in instructions
        assert "instruction" in instructions

    def test_get_next_step(self):
        """Test getting next step"""
        next_step = GuidedModeService.get_next_step(GuidedStep.WELCOME)

        assert next_step == GuidedStep.PASTE_TEXT

    def test_get_next_step_at_end(self):
        """Test getting next step at the end"""
        next_step = GuidedModeService.get_next_step(GuidedStep.COMPLETE)

        assert next_step is None

    def test_get_previous_step(self):
        """Test getting previous step"""
        prev_step = GuidedModeService.get_previous_step(GuidedStep.PASTE_TEXT)

        assert prev_step == GuidedStep.WELCOME

    def test_get_previous_step_at_start(self):
        """Test getting previous step at the start"""
        prev_step = GuidedModeService.get_previous_step(GuidedStep.WELCOME)

        assert prev_step is None

    def test_get_progress(self):
        """Test getting progress"""
        progress = GuidedModeService.get_progress(GuidedStep.PASTE_TEXT)

        assert progress["current_step"] == 2  # Second step
        assert progress["total_steps"] == 6
        assert 0 < progress["percentage"] < 100

    def test_validate_step_completion_empty_text(self):
        """Test validation with empty text"""
        is_valid, error = GuidedModeService.validate_step_completion(
            GuidedStep.PASTE_TEXT,
            {"text": ""}
        )
        
        assert is_valid is False
        assert error is not None

    def test_validate_step_completion_short_text(self):
        """Test validation with short text"""
        is_valid, error = GuidedModeService.validate_step_completion(
            GuidedStep.PASTE_TEXT,
            {"text": "short"}
        )
        
        assert is_valid is False
        assert error is not None

    def test_validate_step_completion_valid_text(self):
        """Test validation with valid text"""
        is_valid, error = GuidedModeService.validate_step_completion(
            GuidedStep.PASTE_TEXT,
            {"text": "This is a long enough text for testing"}
        )
        
        assert is_valid is True
        assert error is None

    def test_get_guided_mode_config(self):
        """Test getting guided mode config"""
        config = GuidedModeService.get_guided_mode_config()
        
        assert config["enabled"] is True
        assert len(config["steps"]) == config["total_steps"]


@pytest.mark.asyncio
class TestGuidedModeRoutes:
    """Test Guided Mode API Routes"""

    async def test_get_guided_config(self, token_helper):
        """Test getting guided config"""
        token = token_helper["token"]
        
        response = client.get(
            "/api/v1/guided/config",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "config" in data

    async def test_get_step_instructions(self, token_helper):
        """Test getting step instructions"""
        token = token_helper["token"]
        
        response = client.get(
            "/api/v1/guided/instructions/welcome",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["step"] == "welcome"
        assert "instructions" in data
        assert "progress" in data

    async def test_next_step_unauthorized(self):
        """Test moving to next step without auth"""
        response = client.post(
            "/api/v1/guided/next",
            json={"step": "welcome", "data": {}}
        )
        
        # Returns 401 Unauthorized instead of 403 Forbidden
        assert response.status_code == 401

    async def test_invalid_step(self, token_helper):
        """Test with invalid step"""
        token = token_helper["token"]
        
        response = client.post(
            "/api/v1/guided/next",
            json={"step": "invalid_step", "data": {}},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
