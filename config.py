import logging
import os
import dotenv
import logging.config


dotenv.load_dotenv()


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    LOG_DIR = os.getenv('LOG_DIR', './logs')
    INTROSPECTION_URI = os.getenv('INTROSPECTION_URI')
    KAFKA_SERVER = os.getenv('KAFKA_SERVER')
    MONGODB_SETTINGS = {
        'db': os.environ['MONGO_DB'],
        'host': os.environ['MONGO_HOST'],
        'port': os.getenv('MONGO_PORT', '27017'),
        'username': os.environ['MONGO_USER'],
        'password': os.environ['MONGO_PASSWORD'],
        'authentication_source': os.getenv('MONGO_AUTH_SRC', 'admin')
    }
    EMAIL = {
        'server': os.getenv('SMTP_SERVER'),
        'ssl_port': int(os.getenv('SMTP_SSL_PORT')),
        'sender': os.getenv('SMTP_SENDER'),
        'username': os.getenv('SMTP_USERNAME'),
        'password': os.getenv('SMTP_PASSWORD')
    }


# Set up logging
if not os.path.exists(Config.LOG_DIR):
    os.mkdir(Config.LOG_DIR)

if not os.path.isdir(Config.LOG_DIR):
    raise ValueError(f'{Config.LOG_DIR} is not a directory')

logging.config.fileConfig('./logging.ini')
