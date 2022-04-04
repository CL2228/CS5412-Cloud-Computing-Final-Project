import smtplib
from email.mime.text import MIMEText
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "cs5412.cl2228@yahoo.com"
SMTP_PASSWORD = "jwmavztrdbudzxgb"
EMAIL_FROM = "cs5412.cl2228@yahoo.com"
EMAIL_TO = "g20170284@icloud.com"
EMAIL_SUBJECT = "REMINDER:"
co_msg = """
Hello, [username]! Just wanted to send a friendly appointment
reminder for your appointment:
[Company]
Where: [companyAddress]
Time: [appointmentTime]
Company URL: [companyUrl]
Change appointment?? Add Service??
change notification preference (text msg/email)

<h1> Heading </h1>
<img src="https://cs5412-final-project.azurewebsites.net/api/httpexample" alt="img">

"""

# jwmavztrdbudzxgb


def send_email():
    msg = MIMEText(co_msg, 'html')
    msg['Subject'] = EMAIL_SUBJECT + "Company - Service at appointmentTime"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    res = mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print(res)
    mail.quit()


if __name__ == '__main__':
    send_email()
