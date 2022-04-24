import copy

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

    # msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="https://www.cuvs.org/sites/default/files/2017-02/a-legacy_3.jpg"><br>Nifty!', 'html')
    msgText = MIMEText('<b>宝 你的男朋友来给你问好了 <i>噢宝</i> 你好</b>.<br><img src="cid:image1"><br>宝!', 'html')

    html_frame = '<html><body>Dear user,</br></br> and an image.</br><img src="{}"><br>END</body></html>'.format("https://cs5412-final-project.azurewebsites.net/api/img-get?name=gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg")
    html_text = 'Dear user,</br></br> and an image.</br><img src="https://cs5412-final-project.azurewebsites.net/api/img-get?name=gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg"><br>Nifty!'.format("MZXCNMCNM")


    print(html_content)
    send_html("test email", email_to, html_content)

