import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock openai and google.generativeai modules if they are not installed or to avoid actual imports during tests if desired,
# but since we installed them, we can mock them in the test.

def test_ai_service_disabled_by_default():
    with patch("app.services.ai.settings.ai.enabled", False):
        from app.services.ai import AIService
        service = AIService()
        assert service.enabled is False
        assert service.generate_explanation({}, []) == ""

def test_ai_service_openai_enabled():
    with patch("app.services.ai.settings.ai.enabled", True), \
         patch("app.services.ai.settings.ai.provider", "openai"), \
         patch("app.services.ai.settings.ai.openai_api_key", "fake_key"), \
         patch("openai.OpenAI") as MockOpenAI:

        from app.services.ai import AIService

        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "AI Summary"
        mock_client.chat.completions.create.return_value = mock_response

        service = AIService()
        assert service.enabled is True
        assert service.openai_client is not None

        summary = service.generate_explanation(
            {"computed_score": 10, "confidence_tier": "A", "rationale": "Test"},
            [{"source_name": "Test", "source_type": "Test", "match_tier": "A", "confidence_score": 0.9}]
        )
        assert summary == "AI Summary"

def test_ai_service_gemini_enabled():
    with patch("app.services.ai.settings.ai.enabled", True), \
         patch("app.services.ai.settings.ai.provider", "gemini"), \
         patch("app.services.ai.settings.ai.gemini_api_key", "fake_key"), \
         patch("google.generativeai.GenerativeModel") as MockGenModel, \
         patch("google.generativeai.configure") as MockConfigure:

        from app.services.ai import AIService

        mock_model = MagicMock()
        MockGenModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Gemini Summary"
        mock_model.generate_content.return_value = mock_response

        service = AIService()
        assert service.enabled is True
        assert service.gemini_model is not None

        summary = service.generate_explanation(
            {"computed_score": 10, "confidence_tier": "A", "rationale": "Test"},
            []
        )
        assert summary == "Gemini Summary"
