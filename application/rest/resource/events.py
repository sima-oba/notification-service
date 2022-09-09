from http import HTTPStatus
from flask import Blueprint, jsonify, request

from domain.service import NotificationService
from ...schema import EventSchema


def get_blueprint(service: NotificationService) -> Blueprint:
    bp = Blueprint('Events', __name__)
    schema = EventSchema()

    @bp.post('/events')
    def create_event():
        event = schema.load(request.json)
        service.notify(event)

        return jsonify({}), HTTPStatus.NO_CONTENT

    return bp
