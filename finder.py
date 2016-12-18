from onliner_by import OnlinerCrawler
import datetime
import settings
from telegram_notifier import TelegramNotifier
import pickle
import os
import logging
import logging.config

logging.config.dictConfig(settings.LOGGER)
LOGGER = logging.getLogger(__name__)
SINCE_FILENAME = os.path.join(settings.BASE_DIR, "last_search.dmp")


def find():
    since = get_since()
    notifier = TelegramNotifier(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)

    cr = OnlinerCrawler(timezone=settings.TIMEZONE)
    LOGGER.info("searching since {}".format(since))
    for apartment in cr.find(since):
        LOGGER.debug(apartment)
        LOGGER.debug("=======")
        notifier.notify(str(apartment))

    save_since()


def get_since():
    if os.path.exists(SINCE_FILENAME):
        return pickle.load(open(SINCE_FILENAME, 'rb'))
    else:
        return datetime.datetime.now(tz=settings.TIMEZONE) - datetime.timedelta(hours=24)


def save_since():
    now = datetime.datetime.now(tz=settings.TIMEZONE)
    pickle.dump(now, open(SINCE_FILENAME, 'wb'))


if __name__ == '__main__':
    find()
    # LOGGER.debug("oloo")
