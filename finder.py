import datetime
import logging.config
import os
import pickle

import settings
from onliner_by import OnlinerCrawler
from telegram_notifier import TelegramNotifier

logging.config.dictConfig(settings.LOGGER)
LOGGER = logging.getLogger(__name__)
SINCE_FILENAME = os.path.join(settings.BASE_DIR, "last_search.dmp")


def find():
    since = get_since()
    notifier = TelegramNotifier(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)

    onliner = OnlinerCrawler(since=since, timezone=settings.TIMEZONE)
    LOGGER.info("searching since {}".format(since))
    for apartment in onliner.find():
        LOGGER.debug(apartment)
        LOGGER.debug("=======")
        notifier.notify(str(apartment))

    save_since()


def get_since():
    if os.path.exists(SINCE_FILENAME):
        return pickle.load(open(SINCE_FILENAME, 'rb'))
    else:
        return datetime.datetime.now(tz=settings.TIMEZONE) - datetime.timedelta(hours=48)


def save_since():
    now = datetime.datetime.now(tz=settings.TIMEZONE)
    pickle.dump(now, open(SINCE_FILENAME, 'wb'))


if __name__ == '__main__':
    find()
