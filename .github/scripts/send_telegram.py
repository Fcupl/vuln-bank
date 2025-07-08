import os
import sys
import requests

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
message = sys.argv[1] if len(sys.argv) > 1 else "Tidak ada pesan."

repo = os.getenv("GITHUB_REPOSITORY") ##
run_id = os.getenv("GITHUB_RUN_ID") ##

message = f"""
🚨 *Pipeline DevSecOps Selesai!*

📦 Secret Scanning (Gitleaks)
🔍 SAST (Semgrep)
📦 SCA (Snyk)
🧪 DAST (ZAP)

📊 Status: *{status_summary}*
🔗 [Lihat detail pipeline](https://github.com/{repo}/actions/runs/{run_id})
"""

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

response = requests.post(url, data=data)
print(f"Telegram response: {response.status_code}")

