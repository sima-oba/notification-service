from http import HTTPStatus
from flask import jsonify, request
from application.schema.template import TemplateSchema
from domain.service.notification import NotificationService


def configure_routes_template(app, service: NotificationService):
    schema = TemplateSchema()

    @app.route('/templates')
    def summary():
        return jsonify(service.summary_templates())

    @app.route('/templates/<string:_id>')
    def get_by_id(_id: str):
        return schema.dump(service.get_template(_id))

    @app.route('/templates', methods=['POST'])
    def add():
        data = schema.load(request.json)
        return service.save_template(data).asdict(), HTTPStatus.CREATED

    @app.route('/templates/<string:_id>', methods=['PUT'])
    def replace(_id: str):
        data = schema.load(request.json)
        template = service.save_template(data, _id)
        return schema.dump(template)

    @app.route('/templates/<string:_id>', methods=['DELETE'])
    def remove(_id: str):
        service.remove_template(_id)
        return {}, HTTPStatus.NO_CONTENT


def configure_routes_email(app, service: NotificationService):

    @app.route('/emails')
    def summary_mail():
        _filter = request.args.to_dict()
        return jsonify(service.summary_emails(_filter))

    @app.route('/emails/<string:_id>')
    def get_mail_by_id(_id: str):
        return jsonify(service.get_email(_id))
