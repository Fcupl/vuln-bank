import os
import requests
from datetime import datetime

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
repo = os.getenv("GITHUB_REPOSITORY")
run_id = os.getenv("GITHUB_RUN_ID")

# Status dari masing-masing tools
ss_result = os.getenv("SS_RESULT", "false").lower()
sca_result = os.getenv("SCA_RESULT", "0")
sast_result = os.getenv("SAST_RESULT", "0")
dast_result = os.getenv("DAST_RESULT", "0")

def icon(ok, label):
    return f"✅ {label}" if ok else f"❌ {label}"

# Interpretasi hasil
secret_scan = icon(ss_result == "false", "Secret Scan: Clean")
sca_status = icon(int(sca_result) == 0, f"SCA: {sca_result} Critical Dependencies")
sast_status = icon(int(sast_result) == 0, f"SAST: {sast_result} High Findings")
dast_status = icon(int(dast_result) == 0, f"DAST: {dast_result} SQLi")

# Format waktu WIB
waktu = datetime.utcnow().timestamp() + (7 * 3600)
timestamp = datetime.fromtimestamp(waktu).strftime("%Y-%m-%d %H:%M WIB")

# Format pesan
message = f"""🚨 *DevSecOps Pipeline Report* 🚨

{secret_scan}  
{sca_status}  
{sast_status}  
{dast_status}

🔗 *Repo:* `{repo}`  
🕐 *Time:* {timestamp}

🔗 [Lihat Pipeline](https://github.com/{repo}/actions/runs/{run_id})  
_Mohon segera ditindaklanjuti!_
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
print("Status Telegram:", response.status_code, response.text)
