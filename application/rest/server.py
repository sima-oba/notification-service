from flask import Flask
from flask_cors import CORS

from domain.service import NotificationService
from infrastructure import database
from infrastructure.repository import NotificationRepository, SMTPSender
from .resource import emails, events, templates
from .encoder import CustomJsonEncoder
from .security import Authorization, Role
from .error import error_bp


URL_PREFIX = '/api/v1/notification'


def create_server(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.json_encoder = CustomJsonEncoder
    app.register_blueprint(error_bp)

    is_auth_enabled = app.config['FLASK_ENV'] != 'development'
    auth = Authorization(config.INTROSPECTION_URI, is_auth_enabled)
    auth.grant_role_for_any_request(Role.ADMIN)
    # auth.require_authorization_for_any_request(app)
    db = database.get_database(config.MONGODB_SETTINGS)

    CORS(app)

    email_sender = SMTPSender(config.EMAIL)
    notification_repo = NotificationRepository(db)
    notification_service = NotificationService(notification_repo, email_sender)

    templates_bp = templates.get_blueprint(notification_service)
    app.register_blueprint(templates_bp, url_prefix=URL_PREFIX)

    emails_bp = emails.get_blueprint(notification_service)
    app.register_blueprint(emails_bp, url_prefix=URL_PREFIX)

    events_bp = events.get_blueprint(notification_service)
    app.register_blueprint(events_bp, url_prefix=URL_PREFIX)

    return app
