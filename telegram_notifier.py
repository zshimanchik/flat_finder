import telebot


class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot = telebot.TeleBot(bot_token)
        self.chat_id = chat_id

    def notify(self, text):
        self.bot.send_message(self.chat_id, text)
