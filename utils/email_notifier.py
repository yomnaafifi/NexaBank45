import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()
class EmailNotifier:
    @staticmethod
    def send_alert(subject: str, body: str):
        """Send email notification using credentials from .env."""
        sender_email = os.getenv("EMAIL_USER")
        receiver_email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("EMAIL_PASSWORD")
        
        if not all([sender_email, receiver_email, password]):
            raise ValueError("Missing email configuration in .env file")
        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            