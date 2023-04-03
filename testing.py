import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("Hello, this is a test email.")

msg['Subject'] = 'Test Email'
msg['From'] = ''
msg['To'] = 'recipient_email_address'

with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
    smtp.login('your_yahoo_email_address', 'your_yahoo_email_password')
    smtp.send_message(msg)