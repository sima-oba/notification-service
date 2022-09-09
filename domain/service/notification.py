import logging
from typing import List, BinaryIO

from ..entity import Email, EmailStatus, EmailTemplate
from ..exception import EntityNotFound, EmailError
from ..repository import INotificationRepository, IEmailSender


_log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        repo: INotificationRepository,
        email_sender: IEmailSender
    ):
        self._repo = repo
        self._email_sender = email_sender

    def summary_emails(self, _filter: dict) -> List[dict]:
        emails = self._repo.find_emails(**_filter)
        return [
            {
                '_id': email._id,
                'created_at': email.created_at,
                'updated_at': email.updated_at,
                'status': email.status,
                'recipient': email.recipient,
                'subject': email.subject
            }
            for email in emails
        ]

    def get_email(self, _id: str) -> Email:
        email = self._repo.find_email_by_id(_id)

        if email is None:
            raise EntityNotFound(Email, f'_id {_id}')

        return email

    def summary_templates(self) -> List[dict]:
        templates = self._repo.find_templates()
        return [
            {
                '_id': template._id,
                'created_at': template.created_at,
                'updated_at': template.updated_at,
                'description': template.description
            }
            for template in templates
        ]

    def get_template(self, _id) -> EmailTemplate:
        template = self._repo.find_template_by_id(_id)

        if template is None:
            raise EntityNotFound(EmailTemplate, f'_id {_id}')

        return template

    def save_template(self, data: dict, _id: str = None) -> EmailTemplate:
        if _id is None:
            return self._repo.add_template(EmailTemplate.new(data))

        template = self.get_template(_id)
        return self._repo.update_template(template.merge(data))

    def remove_template(self, _id: str):
        if not self._repo.remove_template(_id):
            raise EntityNotFound(EmailTemplate, f'_id {_id}')

    def _send_email(
        self,
        subject: str,
        recipient: str,
        template_id: str,
        content: dict,
        attachments: List[BinaryIO] = None
    ) -> Email:
        template = self.get_template(template_id)
        email = Email.new({
            'subject': subject,
            'recipient': recipient,
            'attachments': attachments,
            'content': template.format(content)
        })

        _log.debug(f'sending email to {email.recipient}')

        try:
            self._email_sender.send(email)
            email.status = EmailStatus.SENT
            _log.info(f'email sent to {email.recipient}')
        except EmailError as e:
            email.status = EmailStatus.FAILED
            _log.error(e)

        self._repo.add_email(email)

    def _push_notification(self, **kwargs):
        raise Exception('Not implemented')

    def notify(self, event: dict):
        if event.get('email'):
            self._send_email(**event['email'])

        if event.get('push'):
            self._push_notification(**event['push'])
