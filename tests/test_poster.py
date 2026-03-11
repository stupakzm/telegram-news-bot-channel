# tests/test_poster.py
import pytest
from unittest.mock import patch, MagicMock
from poster import format_post, post_article


SAMPLE_SUMMARY = {
    "id": "https://example.com/1",
    "title": "OpenAI releases GPT-5",
    "summary": "OpenAI launched GPT-5 today.",
    "hashtags": ["#ai", "#techcompanies"],
    "is_important": False,
    "importance_detail": "",
}

IMPORTANT_SUMMARY = {**SAMPLE_SUMMARY, "is_important": True, "importance_detail": "This changes everything."}


def test_format_post_contains_title():
    text = format_post(SAMPLE_SUMMARY, "https://example.com/1")
    assert "OpenAI releases GPT-5" in text


def test_format_post_contains_hashtags():
    text = format_post(SAMPLE_SUMMARY, "https://example.com/1")
    assert "#ai" in text
    assert "#techcompanies" in text


def test_format_post_contains_url():
    text = format_post(SAMPLE_SUMMARY, "https://example.com/1")
    assert "https://example.com/1" in text


@patch("poster.requests.post")
def test_post_article_calls_telegram(mock_post):
    mock_post.return_value.json.return_value = {"ok": True, "result": {"message_id": 42}}
    mock_post.return_value.raise_for_status = MagicMock()
    msg_id = post_article(SAMPLE_SUMMARY, bot_token="tok", channel_id="@ch")
    mock_post.assert_called_once()
    assert msg_id == 42


@patch("poster.requests.post")
def test_post_article_sends_followup_for_important(mock_post):
    mock_post.return_value.json.return_value = {"ok": True, "result": {"message_id": 99}}
    mock_post.return_value.raise_for_status = MagicMock()
    post_article(IMPORTANT_SUMMARY, bot_token="tok", channel_id="@ch")
    assert mock_post.call_count == 2  # main post + follow-up reply


@patch("poster.requests.post")
def test_post_article_no_followup_for_unimportant(mock_post):
    mock_post.return_value.json.return_value = {"ok": True, "result": {"message_id": 55}}
    mock_post.return_value.raise_for_status = MagicMock()
    post_article(SAMPLE_SUMMARY, bot_token="tok", channel_id="@ch")
    assert mock_post.call_count == 1
