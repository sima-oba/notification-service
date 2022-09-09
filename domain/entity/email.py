from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional

from .entity import Entity


class EmailStatus(IntEnum):
    SENT = 0
    FAILED = 1


@dataclass
class Attachment:
    filename: str
    data: str


@dataclass
class Email(Entity):
    status: Optional[EmailStatus]
    subject: str
    recipient: List[str]
    content: str
    attachments: Optional[List[Attachment]]
