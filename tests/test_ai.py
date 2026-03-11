# tests/test_ai.py
import pytest
import json
from unittest.mock import patch, MagicMock
from ai import summarize_articles, _call_gemini, _call_groq, _build_prompt


SAMPLE_ARTICLES = [
    {
        "url": "https://example.com/1",
        "title": "OpenAI releases GPT-5",
        "description": "OpenAI today announced GPT-5 with major reasoning upgrades.",
        "category": "#ai",
    }
]

SAMPLE_RESPONSE = json.dumps([
    {
        "id": "https://example.com/1",
        "title": "OpenAI releases GPT-5",
        "summary": "OpenAI launched GPT-5 today with major reasoning upgrades.",
        "hashtags": ["#ai", "#techcompanies"],
        "is_important": True,
        "importance_detail": "This marks a significant shift in the AI landscape.",
    }
])


def test_build_prompt_contains_article_title():
    prompt = _build_prompt(SAMPLE_ARTICLES)
    assert "OpenAI releases GPT-5" in prompt


def test_build_prompt_contains_json_instruction():
    prompt = _build_prompt(SAMPLE_ARTICLES)
    assert "JSON" in prompt


@patch("ai.genai")
def test_call_gemini_returns_parsed_json(mock_genai):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = SAMPLE_RESPONSE
    mock_genai.GenerativeModel.return_value = mock_model
    result = _call_gemini(SAMPLE_ARTICLES, api_key="fake")
    assert result[0]["title"] == "OpenAI releases GPT-5"
    assert result[0]["is_important"] is True


@patch("ai.requests.post")
def test_call_groq_returns_parsed_json(mock_post):
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": SAMPLE_RESPONSE}}]
    }
    mock_post.return_value.raise_for_status = MagicMock()
    result = _call_groq(SAMPLE_ARTICLES, api_key="fake")
    assert result[0]["id"] == "https://example.com/1"


@patch("ai._call_gemini")
@patch("ai._call_groq")
def test_summarize_uses_gemini_first(mock_groq, mock_gemini):
    mock_gemini.return_value = [{"id": "x"}]
    result = summarize_articles(SAMPLE_ARTICLES, gemini_key="g", groq_key="r")
    mock_gemini.assert_called_once()
    mock_groq.assert_not_called()


@patch("ai._call_gemini", side_effect=Exception("gemini down"))
@patch("ai._call_groq")
def test_summarize_falls_back_to_groq(mock_groq, mock_gemini):
    mock_groq.return_value = [{"id": "x"}]
    result = summarize_articles(SAMPLE_ARTICLES, gemini_key="g", groq_key="r")
    mock_groq.assert_called_once()
