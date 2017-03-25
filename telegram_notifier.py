import requests


class TelegramNotifier:
    _BASE_URL = 'https://api.telegram.org/bot{token}/{method}'

    def __init__(self, bot_token, chat_id):
        self._send_message_url = self._BASE_URL.format(token=bot_token,
                                                       method='sendMessage')
        self._chat_id = chat_id

    def notify(self, text):
        data = {
            'chat_id': self._chat_id,
            'text': text,
        }
        requests.post(self._send_message_url, json=data)
