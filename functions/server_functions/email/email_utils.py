# from functions.server_functions.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
from ..config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


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


def send_html(subject: str, to: str, html_content: str, img_bytes: bytes, debug: bool = True):
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

        msg_image = MIMEImage(img_bytes)
        msg_image.add_header('Content-ID', '<image1>')
        msgRoot.attach(msg_image)

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
    <img src="cid:image1"></br>.
    </body>
    </html>
    """.format("G01", "GatesHall", "2022-4-24")

    # print(html_content)
    fp = open("./lch.png", "rb")
    data = fp.read()
    print(data)
    send_html("test email", email_to, html_content, data)

