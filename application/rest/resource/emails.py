from flask import Blueprint, jsonify, request

from domain.service import NotificationService


def get_blueprint(service: NotificationService) -> Blueprint:
    bp = Blueprint('Emails', __name__)

    @bp.get('/emails')
    def summary():
        _filter = request.args.to_dict()
        return jsonify(service.summary_emails(_filter))

    @bp.get('/emails/<string:_id>')
    def get_by_id(_id: str):
        return jsonify(service.get_email(_id))

    return bp
