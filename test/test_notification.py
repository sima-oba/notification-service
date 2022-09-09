from flask import Flask
from itsdangerous import json
import pytest
from infrastructure.database import get_database
from infrastructure.repository import (
    SMTPSender,
    NotificationRepository
)
from handlers.route_handlers import (
    configure_routes_email,
    configure_routes_template
)
from domain.service import NotificationService
from . import TestConfig as config


URL_PREFIX = '/api/v1/notification'
db = get_database(config.MONGODB_SETTINGS)
email_sender = SMTPSender(config.EMAIL)
notification_repo = NotificationRepository(db)
notification_service = NotificationService(notification_repo, email_sender)


@pytest.fixture
def clientinstance():
    app = Flask(__name__)
    configure_routes_email(app, notification_service)
    configure_routes_template(app, notification_service)
    client = app.test_client()
    return client


@pytest.fixture
def postTemplate(clientinstance):
    url = '/templates'
    data = {
        "description": "",
        "template": ""
    }
    posting = clientinstance.post(url, json=data)
    return posting.get_data(), posting.status_code


def _test_templates_route(clientinstance):
    url = '/templates'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def _test_template_id(clientinstance, postTemplate):
    data, code = postTemplate
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/templates/{_id}'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200 and code == 201


def _test_template_post(postTemplate):
    data, code = postTemplate

    assert data != b''
    assert code == 201


def _test_template_put(clientinstance, postTemplate):
    data, code = postTemplate
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/templates/{_id}'

    data = {
        "description": "",
        "template": ""
    }

    response = clientinstance.put(url, json=data)
    assert response.get_data() != b''
    assert response.status_code == 200 and code == 201


def _test_template_delete(clientinstance, postTemplate):
    data, code = postTemplate
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/templates/{_id}'

    response = clientinstance.delete(url)
    assert response.status_code == 204 and code == 201


def _test_email_route(clientinstance):
    url = '/emails'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200
