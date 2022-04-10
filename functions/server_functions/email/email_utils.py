# from functions.server_functions.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
from ..config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
import smtplib
from email.mime.text import MIMEText


def send(subject: str,
         to: str,
         content,
         content_type: str = 'plain',
         debug: bool = True):
    msg = MIMEText(content, content_type)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = to

    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debug)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, to, msg.as_string())
    mail.quit()

