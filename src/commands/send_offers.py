from typing import List
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

def send_offers_by_email(body: str) -> None:
 
    msg = MIMEMultipart()
    from_email = "nikey_es@yahoo.es"
    to_email = "evamoga@gmail.com, nikey_es@yahoo.es"
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Portaventura Daily Digest " + date.today().strftime("%Y-%m-%d")
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        smtp_key = os.environ.get('BREVO_SMTP_KEY')
        server.login(from_email, smtp_key)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print('Something went wrong while sending email:', e)
        