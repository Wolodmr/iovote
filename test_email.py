import smtplib
from email.mime.text import MIMEText

# Replace with your email details
SMTP_SERVER = "smtp.gmail.com"  # Change if using another provider
SMTP_PORT = 587
EMAIL_ADDRESS = "postvezha@gmail.com"  # Your sender email
EMAIL_PASSWORD = "sneoojkhwotisdhz"  # Use App Password, NOT regular password
RECIPIENT = "postvezha@gmail.com"

# Create the email
msg = MIMEText("Test email from Python")
msg["Subject"] = "Test Email"
msg["From"] = EMAIL_ADDRESS
msg["To"] = RECIPIENT

try:
    # Connect and send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, RECIPIENT, msg.as_string())
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error sending email: {e}")
