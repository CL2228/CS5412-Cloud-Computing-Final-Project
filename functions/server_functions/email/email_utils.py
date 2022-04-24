# from functions.server_functions.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
from ..config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_plain_text(subject: str,
         to: str,
         content,
         content_type: str = 'plain',
         debug: bool = True):
    try:
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
        return True
    except Exception:
        return False


def send_html(subject: str, to: str, html_content: str, debug: bool = True):
    try:
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = EMAIL_FROM
        msgRoot['to'] = to
        msgRoot.preamble = "This is a multi-part message in MIME format."

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(html_content, 'html')
        msgAlternative.attach(msgText)

        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.set_debuglevel(debug)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(EMAIL_FROM, to, msgRoot.as_string())
        mail.quit()
    except Exception as ex:
        print(ex)
        return False


if __name__ == "__main__":
    email_to = "g20170284@icloud.com"

    html_content = """
    <html>
    <body>
    Dear user, </br></br>
    There is a suspicious entrance record of your apartment <b>{}, {}</b> at <i>{}</i>. 
    Here is the photo taken from this record. Please log in to our system to check if action needed.</br></br>
    Thanks.</br>
    CL<br>
    <img src="{}"></br>.
    </body>
    </html>
    """.format("G01", "GatesHall", "2022-4-24", "https://cs5412-final-project.azurewebsites.net/api/img-get?name=gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg")

    print(html_content)
    send_html("test email", email_to, html_content)

