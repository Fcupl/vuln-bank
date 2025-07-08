import os
import requests
from datetime import datetime

# Fungsi bantu emoji ✅❌
def icon(condition, text_ok, text_fail=None):
    if condition:
        return f"✅ {text_ok}"
    else:
        return f"❌ {text_fail or text_ok}"

def safe_int(val):
    try:
        return int(val)
    except:
        return -1

# Ambil data dari environment variables
sca_result = os.getenv("SCA_FINDINGS", "")
sast_result = os.getenv("SAST_FINDINGS", "")
dast_result = os.getenv("DAST_FINDINGS", "")
gitleaks_result = os.getenv("GITLEAKS_STATUS", "")

repo = os.getenv("GITHUB_REPOSITORY", "Unknown Repo")
runtime = datetime.now().strftime("%Y-%m-%d %H:%M WIB")
run_url = f"https://github.com/{repo}/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}"

# Konversi hasil masing-masing
sca_status = icon(safe_int(sca_result) == 0, "SCA: Clean", f"SCA: {sca_result} Critical Dependencies")
sast_status = icon(safe_int(sast_result) == 0, "SAST: Clean", f"SAST: {sast_result} High Findings")
dast_status = icon(safe_int(dast_result) == 0, "DAST: Clean", f"DAST: {dast_result} Warnings")
gitleaks_status = icon(gitleaks_result == "success", "Secret Scan: Clean", "Secret Scan: Findings Detected")

# Bangun pesan Telegram
message = f"""
🚨 *DevSecOps Pipeline Report* 🚨

{gitleaks_status}  
{sca_status}  
{sast_status}  
{dast_status}

🔗 *Repo:* `{repo}`  
🕐 *Time:* {runtime}  
🔗 [Lihat detail pipeline]({run_url})

Mohon segera ditindaklanjuti!
"""

# Kirim ke Telegram
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

response = requests.post(url, data=data)
print(f"Telegram response: {response.status_code} {response.text}")
