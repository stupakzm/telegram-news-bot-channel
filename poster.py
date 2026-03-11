# poster.py
import requests


TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


def format_post(summary: dict, url: str) -> str:
    hashtags = " ".join(summary["hashtags"])
    return (
        f"🔹 *{summary['title']}*\n\n"
        f"{summary['summary']}\n\n"
        f"{hashtags}\n"
        f"🔗 {url}"
    )


def _send_message(bot_token: str, channel_id: str, text: str, reply_to: int = None) -> int:
    payload = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to

    resp = requests.post(
        TELEGRAM_API.format(token=bot_token, method="sendMessage"),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["result"]["message_id"]


def post_article(summary: dict, bot_token: str, channel_id: str) -> int:
    text = format_post(summary, summary["id"])
    msg_id = _send_message(bot_token, channel_id, text)

    if summary.get("is_important") and summary.get("importance_detail"):
        followup = f"🧵 *Why this matters:*\n{summary['importance_detail']}"
        _send_message(bot_token, channel_id, followup, reply_to=msg_id)

    return msg_id
