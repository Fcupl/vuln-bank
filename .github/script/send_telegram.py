import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Pesan yang akan dikirim
message = """
🚨 *DevSecOps Alert - vuln-bank*

🔐 Secret Scanning: ✅
📦 SCA (Library check): ✅
🔍 SAST (Code analysis): ✅
🧪 DAST (Runtime test): ✅

Silakan cek hasil lengkap di CI/CD pipeline.
"""

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Pesan Telegram berhasil dikirim.")
    else:
        print("Gagal kirim Telegram:", response.text)

if __name__ == "__main__":
    if not BOT
