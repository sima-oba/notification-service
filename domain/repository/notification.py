from abc import ABC, abstractmethod
from typing import List, Optional

from ..entity import Email, EmailTemplate


class INotificationRepository(ABC):
    @abstractmethod
    def find_emails(self, **_filter) -> List[Email]:
        pass

    @abstractmethod
    def find_email_by_id(self, _id: str) -> Optional[Email]:
        pass

    @abstractmethod
    def add_email(self, email: Email) -> Email:
        pass

    @abstractmethod
    def find_templates(self) -> List[EmailTemplate]:
        pass

    @abstractmethod
    def find_template_by_id(self, _id: str) -> Optional[EmailTemplate]:
        pass

    @abstractmethod
    def add_template(self, template: EmailTemplate) -> EmailTemplate:
        pass

    @abstractmethod
    def update_template(
        self, template: EmailTemplate
    ) -> Optional[EmailTemplate]:
        pass

    @abstractmethod
    def remove_template(self, _id: str) -> bool:
        pass
