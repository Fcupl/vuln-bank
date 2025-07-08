import os
import requests
import sys

status = sys.argv[1] if len(sys.argv) > 1 else "❓ Status tidak diketahui"
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

message = f"""
📢 *Laporan DevSecOps*

Status pipeline: {status}

🔍 Secret Scan (Gitleaks)
🧠 SAST (Semgrep)
📦 SCA (Snyk)
🧪 DAST (ZAP)

Cek GitHub Actions untuk detail lengkap.
"""

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    'chat_id': chat_id,
    'text': message,
    'parse_mode': 'Markdown'
}

r = requests.post(url, data=payload)
print(r.status_code, r.text)
