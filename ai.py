# ai.py
import json
import requests
import google.generativeai as genai
from config import GEMINI_MODEL, GROQ_MODEL, GROQ_API_URL


def _build_prompt(articles: list) -> str:
    articles_text = "\n\n".join(
        f"ID: {a['url']}\nTitle: {a['title']}\nDescription: {a['description']}\nCategory: {a['category']}"
        for a in articles
    )
    return f"""You are a tech news editor. Analyze these articles and return a JSON array.

For each article:
- summary: 2-3 punchy sentences, no fluff, no marketing speak
- hashtags: pick 1-2 most relevant from [#tech, #ai, #privacy, #software, #techcompanies, #hardware]
- is_important: true ONLY if this has major real-world impact on a field, company, region, or market
- importance_detail: if is_important is true, write one paragraph with deeper context; otherwise empty string

Return ONLY valid JSON array. No markdown. No explanation. No code fences.

Articles:
{articles_text}

Required JSON schema per item:
{{
  "id": "<article url>",
  "title": "<original title>",
  "summary": "<2-3 sentences>",
  "hashtags": ["#tag1", "#tag2"],
  "is_important": true/false,
  "importance_detail": "<paragraph or empty string>"
}}"""


def _call_gemini(articles: list, api_key: str) -> list:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(_build_prompt(articles))
    return json.loads(response.text)


def _call_groq(articles: list, api_key: str) -> list:
    resp = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": _build_prompt(articles)}],
            "temperature": 0.3,
        },
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def summarize_articles(articles: list, gemini_key: str, groq_key: str) -> list:
    try:
        return _call_gemini(articles, gemini_key)
    except Exception as e:
        print(f"[ai] Gemini failed ({e}), falling back to Groq...")
        return _call_groq(articles, groq_key)
