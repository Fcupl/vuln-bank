import os
import sys
import requests

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
repo = os.getenv("GITHUB_REPOSITORY")
run_id = os.getenv("GITHUB_RUN_ID")

message_body = sys.argv[1] if len(sys.argv) > 1 else "❌ Tidak ada status"

message = (
    "*📢 Pipeline DevSecOps Selesai!*\n"
    "\n"
    f"{message_body}\n"
    "\n"
    f"[🔗 Lihat detail pipeline](https://github.com/{repo}/actions/runs/{run_id})"
)

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

response = requests.post(url, data=data)

# Debug info
print("CHAT_ID:", chat_id)
print("RESPONSE:", response.status_code)
print(response.text)
