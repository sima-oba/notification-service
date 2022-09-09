import base64
import binascii
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

from domain.entity import Email
from domain.entity.email import Attachment
from domain.exception import EmailError
from domain.repository import IEmailSender


class SMTPSender(IEmailSender):
    def __init__(self, config: dict) -> None:
        self._server = config['server']
        self._port = config['ssl_port']
        self._sender = config['sender']
        self._username = config['username']
        self._password = config['password']

    def send(self, email: Email):
        msg = MIMEMultipart()
        msg['From'] = self._sender
        msg['To'] = ','.join(email.recipient)
        msg['Subject'] = email.subject
        msg.attach(MIMEText(email.content, 'html'))

        if email.attachments:
            for attachment in email.attachments:
                msg.attach(self._make_attachment(attachment))

        try:
            server = SMTP_SSL(self._server, self._port)
            server.ehlo()
            server.login(self._username, self._password)
            server.sendmail(self._sender, email.recipient, msg.as_string())
            server.close()
        except SMTPException as e:
            raise EmailError(e)

    def _make_attachment(self, attachment: Attachment) -> MIMEBase:
        try:
            data = base64.b64decode(attachment.data)
        except binascii.Error as e:
            raise EmailError(e)

        disposition = f'attachment; filename={attachment.filename}'
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(data)
        part.add_header('Content-Disposition', disposition)
        encoders.encode_base64(part)

        return part
