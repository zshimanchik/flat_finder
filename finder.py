import datetime
import logging.config
import os
import pickle

import neagent
import settings
from onliner_by import OnlinerCrawler
from telegram_notifier import TelegramNotifier

logging.config.dictConfig(settings.LOGGER)
LOGGER = logging.getLogger(__name__)
SINCE_FILENAME = os.path.join(settings.BASE_DIR, "last_search.dmp")


def find():
    notifier = TelegramNotifier(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)

    since = get_since()
    crawlers = [
        OnlinerCrawler(since=since, timezone=settings.TIMEZONE),
        neagent.Neagent(),
    ]

    for crawler in crawlers:
        LOGGER.info("searching using crawler: {}".format(crawler.__class__.__name__))
        for apartment in crawler.find():
            LOGGER.debug(apartment)
            LOGGER.debug("=======")
            notifier.notify(str(apartment))


def get_since():
    if os.path.exists(SINCE_FILENAME):
        since = pickle.load(open(SINCE_FILENAME, 'rb'))
    else:
        since = datetime.datetime.now(tz=settings.TIMEZONE) - datetime.timedelta(hours=48)

    now = datetime.datetime.now(tz=settings.TIMEZONE)
    pickle.dump(now, open(SINCE_FILENAME, 'wb'))
    return since


if __name__ == '__main__':
    find()
