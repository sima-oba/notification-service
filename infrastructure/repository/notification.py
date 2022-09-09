from pymongo.database import Database
from dacite.config import Config
from dacite.core import from_dict
from typing import List, Optional

from domain.entity import Email, EmailTemplate
from domain.entity.email import EmailStatus
from domain.repository import INotificationRepository


class NotificationRepository(INotificationRepository):
    def __init__(self, db: Database):
        self._emails = db['email']
        self._templates = db['email_template']

    def _email_from_dict(self, doc: dict) -> Email:
        return from_dict(Email, doc, config=Config(cast=[EmailStatus]))

    def find_emails(self, **_filter) -> List[Email]:
        docs = self._emails.find(_filter)
        return [self._email_from_dict(doc) for doc in docs]

    def find_email_by_id(self, _id: str) -> Optional[Email]:
        doc = self._emails.find_one({'_id': _id})
        return self._email_from_dict(doc) if doc else None

    def add_email(self, email: Email) -> Email:
        self._emails.insert_one(email.asdict())
        return email

    def find_templates(self) -> List[EmailTemplate]:
        docs = self._templates.find()
        return [from_dict(EmailTemplate, doc) for doc in docs]

    def find_template_by_id(self, _id: str) -> Optional[EmailTemplate]:
        doc = self._templates.find_one({'_id': _id})
        return from_dict(EmailTemplate, doc) if doc else None

    def add_template(self, template: EmailTemplate) -> EmailTemplate:
        result = self._templates.insert_one(template.asdict())
        template._id = result.inserted_id
        return template

    def update_template(
        self, template: EmailTemplate
    ) -> Optional[EmailTemplate]:
        _filter = {'_id': template._id}
        operation = {'$set': template.asdict()}
        result = self._templates.update_one(_filter, operation)
        return template if result.matched_count > 0 else None

    def remove_template(self, _id: str) -> bool:
        result = self._templates.delete_one({'_id': _id})
        return result.deleted_count > 0
