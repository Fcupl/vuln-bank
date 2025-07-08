import os
import smtplib
from email.mime.text import MIMEText

smtp_server = os.environ["EMAIL_SMTP_SERVER"]
smtp_port = int(os.environ["EMAIL_SMTP_PORT"])
sender_email = os.environ["EMAIL_SENDER_ADDRESS"]
sender_password = os.environ["EMAIL_SENDER_PASSWORD"]
receiver_email = os.environ["EMAIL_RECEIVER_ADDRESS"]

subject = "🔒 DevSecOps Scan Report - vuln-bank"
body = """
Hello,

Berikut adalah hasil scan DevSecOps otomatis untuk project *vuln-bank*:

✅ Secret Scan
✅ SCA (Software Composition Analysis)
✅ SAST (Static Analysis)
✅ DAST (Dynamic Test)

Silakan login ke GitHub Actions untuk melihat detail hasilnya.

Salam,
Bot Fahri Security Pipeline
"""

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("Email sent successfully to", receiver_email)
except Exception as e:
    print("Failed to send email:", str(e))
