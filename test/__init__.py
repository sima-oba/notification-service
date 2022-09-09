class TestConfig:
    """Set Flask configuration variables."""

    TESTING = True

    # General Config
    SECRET_KEY = 'secretkey'
    FLASK_ENV = 'development'
    SERVER_NAME = 'localhost.localdomain'

    # Mongo
    MONGODB_SETTINGS = {
        'db': 'testdb',
        'host': 'localhost',
        'port': 27017,
        'mock': True,
    }
    EMAIL = {
        'server': 'smtp.gmail.com',
        'ssl_port': '465',
        'sender': 'johndoe@email.com',
        'username': 'johndoe@email.com',
        'password': '1q2w3e4r'
    }
    KAFKA_SERVER = "localhost:9092"
    APM_SERVER_URL = '192.168.1.11'
    APM_SECRET_TOKEN = '12345'
