import os
import requests
import json
from datetime import datetime

repo = os.getenv("GITHUB_REPOSITORY", "unknown")
run_id = os.getenv("GITHUB_RUN_ID", "0")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M WIB")

secret_summary = "Clean"
sca_summary = "0 Critical Dependencies"
sast_summary = "0 High Findings"
dast_summary = "No Issues Detected"

sca_status_emoji = "✅"
sast_status_emoji = "✅"
dast_status_emoji = "✅"

try:
    with open("artifacts/gitleaks-report/gitleaks-report.json") as f:
        data = json.load(f)
        if len(data) > 0:
            secret_summary = f"{len(data)} Secrets Found"
        else:
            secret_summary = "Clean"
except:
    secret_summary = "❌ Gagal parsing gitleaks"

try:
    with open("artifacts/semgrep-report/semgrep.sarif") as f:
        sarif = json.load(f)
        findings = [r for r in sarif["runs"][0]["results"] if r["level"] == "error" or r["level"] == "warning"]
        count = len(findings)
        if count > 0:
            sast_status_emoji = "❌"
            sast_summary = f"{count} High Findings"
except:
    sast_summary = "❌ Gagal parsing semgrep"

try:
    snyk_findings = 2  # <- nanti bisa parsing log hasil run snyk
    if snyk_findings > 0:
        sca_status_emoji = "❌"
        sca_summary = f"{snyk_findings} Critical Dependencies"
except:
    sca_summary = "❌ Gagal parsing snyk"

try:
    with open("artifacts/zap-report/zap-report.json") as f:
        data = json.load(f)
        alerts = data.get("site", [])[0].get("alerts", [])
        if alerts:
            dast_status_emoji = "❌"
            dast_summary = "SQL Injection Detected" if any("SQL" in a["name"] for a in alerts) else "Vulnerabilities Found"
except:
    dast_summary = "❌ Gagal parsing ZAP"

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

message = f"""
🚨 *DevSecOps Pipeline Report* 🚨

✅ Secret Scan: {secret_summary}
{sca_status_emoji} SCA: {sca_summary}
{sast_status_emoji} SAST: {sast_summary}
{dast_status_emoji} DAST: {dast_summary}

🔗 Repo: {repo}
🕐 Time: {timestamp}

Mohon segera ditindaklanjuti!
"""

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown"
}

r = requests.post(url, data=data)
print("Telegram response:", r.status_code)
