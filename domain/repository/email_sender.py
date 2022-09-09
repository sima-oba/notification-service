from abc import ABC, abstractmethod

from ..entity import Email


class IEmailSender(ABC):
    @abstractmethod
    def send(self, email: Email):
        pass
