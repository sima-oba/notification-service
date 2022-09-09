from domain.service import NotificationService
from infrastructure import database
from infrastructure.repository import NotificationRepository, SMTPSender
from .consumer import EventConsumer


def start_consumer(config):
    db = database.get_database(config.MONGODB_SETTINGS)
    kafka_config = {
        'bootstrap.servers': config.KAFKA_SERVER,
        'group.id': 'NOTIFICATION',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    }

    email_sender = SMTPSender(config.EMAIL)
    notification_repo = NotificationRepository(db)
    notification_service = NotificationService(notification_repo, email_sender)

    event_consumer = EventConsumer(notification_service)
    event_consumer.start(kafka_config, 'NOTIFICATION')
    event_consumer.wait()
