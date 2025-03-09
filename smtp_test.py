import smtplib

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "postvezha@gmail.com"
EMAIL_HOST_PASSWORD = "ljosehygsmlcunls"  # Replace with your actual app password

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()  # Secure the connection
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("✅ SMTP Login Successful!")
    server.quit()
except Exception as e:
    print(f"❌ SMTP Login Failed: {e}")