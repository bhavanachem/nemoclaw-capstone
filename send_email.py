import json
import smtplib
from email.message import EmailMessage
from pathlib import Path

config = json.loads(
    Path("/sandbox/hand/gmail_config.json").read_text(encoding="utf-8")
)
message = EmailMessage()
message["From"] = config["email"]
message["To"] = config["email"]
message["Subject"] = "NemoClaw Gmail policy test"
message.set_content("Sent through the NemoClaw Gmail policy preset.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
    smtp.login(config["email"], config["app_password"])
    smtp.send_message(message)
