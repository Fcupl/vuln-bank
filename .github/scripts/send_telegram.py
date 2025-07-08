import os
import sys
import requests

# Ambil token dan chat ID dari secret environment
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Ambil status summary dari argumen pertama
status_summary = sys.argv[1] if len(sys.argv) > 1 else "🚫 Tidak ada status yang dikirim."

# Ambil informasi dari environment GitHub
repo = os.getenv("GITHUB_REPOSITORY", "unknown/repo")
run_id = os.getenv("GITHUB_RUN_ID", "0")

# Buat pesan dengan Markdown dan newline (\n)
message = f"""
📢 *Pipeline DevSecOps Selesai!*

{status_summary}

🔗 [Lihat detail pipeline](https://github.com/{repo}/actions/runs/{run_id})
"""

# Kirim ke Telegram
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

response = requests.post(url, data=data)

# Debug hasil
print(f"Telegram response: {response.status_code}")
print(response.text)
