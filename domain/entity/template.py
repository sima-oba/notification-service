import re
from dataclasses import dataclass

from .entity import Entity


@dataclass
class EmailTemplate(Entity):
    template: str
    description: str

    def format(self, content: dict) -> str:
        placeholders = {'{{' + k + '}}': v for k, v in content.items()}
        pattern = re.compile('|'.join(placeholders.keys()))

        return pattern.sub(
            lambda match: placeholders[match.group(0)], self.template
        )
