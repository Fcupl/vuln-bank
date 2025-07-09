import os
import requests
from datetime import datetime


bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")


secret_status = os.getenv("GITLEAKS_STATUS", "Unknown")
sca_issues = os.getenv("SCA_FINDINGS", "Unknown")
sast_issues = os.getenv("SAST_FINDINGS", "Unknown")
dast_issues = os.getenv("DAST_FINDINGS", "Unknown")

repo = os.getenv("GITHUB_REPOSITORY", "Unknown")
run_id = os.getenv("GITHUB_RUN_ID", "")
pipeline_url = f"https://github.com/{repo}/actions/runs/{run_id}"


now = datetime.utcnow()
time_wib = now.replace(hour=(now.hour + 7) % 24)
wib_str = time_wib.strftime("%Y-%m-%d %H:%M WIB")


def status_line(label, value):
    if value in ["0", "success", "✅"]:
        return f"✅ {label}: Clean"
    elif value.lower() == "unknown":
        return f"⚠️ {label}: Unknown"
    else:
        return f"❌ {label}: {value}"


message = f"""
🚨 *DevSecOps Pipeline Report* 🚨

{status_line("Secret Scan", secret_status)}
{status_line("SCA", sca_issues + " Critical Dependencies")}
{status_line("SAST", sast_issues + " High Findings")}
{status_line("DAST", dast_issues + " Warnings")}

🔗 *Repo*: {repo}  
🕐 *Time*: {wib_str}  
🔗 [Lihat detail pipeline]({pipeline_url})

*Mohon segera ditindaklanjuti!*
"""


url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}

response = requests.post(url, data=data)
print(f"Telegram response: {response.status_code} - {response.text}")
