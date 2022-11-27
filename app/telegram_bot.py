import telegram


class TelegramBot():
    def __init__(self, api_key):
        self.token = api_key
        self.telegram_bot = None

    def get_bot(self):
        if(self.telegram_bot is None):
            base_url = 'https://api.telegram.org/bot' + self.token + '/'
            data = {"url": ""}
            self.telegram_bot = telegram.Bot(token=self.token)
        return self.telegram_bot

    def send_message(self, *args, **kwargs):
        self.get_bot().send_message(*args, **kwargs)

    def send_photo(self, *args, **kwargs):
        self.get_bot().send_photo(*args, **kwargs)
