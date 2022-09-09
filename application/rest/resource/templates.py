from http import HTTPStatus
from flask import Blueprint, jsonify, request

from domain.service import NotificationService
from ...schema import TemplateSchema


def get_blueprint(service: NotificationService) -> Blueprint:
    bp = Blueprint('Templates', __name__)
    schema = TemplateSchema()

    @bp.get('/templates')
    def summary():
        return jsonify(service.summary_templates())

    @bp.get('/templates/<string:_id>')
    def get_by_id(_id: str):
        return schema.dump(service.get_template(_id))

    @bp.post('/templates')
    def add():
        data = schema.load(request.json)
        template = schema.dump(service.save_template(data))
        return template, HTTPStatus.CREATED

    @bp.put('/templates/<string:_id>')
    def replace(_id: str):
        data = schema.load(request.json)
        template = service.save_template(data, _id)
        return schema.dump(template)

    @bp.delete('/templates/<string:_id>')
    def remove(_id: str):
        service.remove_template(_id)
        return {}, HTTPStatus.NO_CONTENT

    return bp
