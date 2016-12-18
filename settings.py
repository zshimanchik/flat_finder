import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TELEGRAM_BOT_TOKEN = os.environ.get('FLAT_FINDER_BOT_TOKEN')
if TELEGRAM_BOT_TOKEN is None:
    raise Exception("Environment variable FLAT_FINDER_BOT_TOKEN is not found!")

TELEGRAM_CHAT_ID = os.environ.get('FLAT_FINDER_CHAT_ID')
if TELEGRAM_CHAT_ID is None:
    raise Exception("Environment variable FLAT_FINDER_CHAT_ID is not found!")

TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))

LOGGER = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}