from marshmallow import Schema, fields


class _Attachment(Schema):
    filename = fields.String(required=True)
    data = fields.String(required=True)


class _EmailSchema(Schema):
    subject = fields.String(required=True)
    recipient = fields.List(fields.Email, required=True)
    content = fields.Dict(required=True)
    attachments = fields.List(fields.Nested(_Attachment), missing=None)
    template_id = fields.String(required=True)


class _PushSchema(Schema):
    pass


class EventSchema(Schema):
    email = fields.Nested(_EmailSchema, missing=None)
    push = fields.Nested(_PushSchema, missing=None)
