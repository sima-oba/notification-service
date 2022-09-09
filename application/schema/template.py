import base64
from marshmallow import Schema, fields, post_load, pre_dump

from domain.entity.template import EmailTemplate


class TemplateSchema(Schema):
    template = fields.String(required=True)
    description = fields.String(required=True)

    @post_load
    def decode_base64(self, data: dict, **kwargs) -> dict:
        data['template'] = base64.b64decode(data['template']).decode('utf8')
        return data

    @pre_dump
    def encode_base64(self, obj: EmailTemplate, **kwargs) -> dict:
        data = obj.asdict()
        data['template'] = base64.b64encode(data['template'].encode('utf8'))
        return data
