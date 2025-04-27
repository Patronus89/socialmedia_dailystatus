# email_sender.py
# SMTP email sending logic here
# email_sender.py
import smtplib
from email.message import EmailMessage
import os

def send_email_report(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(body)

        # Attach the report
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")

print("Sending report email...")