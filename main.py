from aiogram.utils import executor
from settings.init_tg_bot import dp
from telegramClient import telegramClient
from threading import Thread
import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slackClient.slackClient import app
from settings.init_slack_bot import slack_app_token

def start_slack():
    SocketModeHandler(app, slack_app_token).start()

    

if __name__ == "__main__":
    thread1 = Thread(target=start_slack, args=(), daemon=True)
    thread1.start()
    telegramClient.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates = True)


