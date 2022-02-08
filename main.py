from aiogram.utils import executor
from settings.init_tg_bot import dp
from telegramClient import telegramClient
from threading import Thread
import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slackClient.slackClient import app, send_pair
from settings.init_slack_bot import slack_app_token
from neo4jdb.db import db
import schedule
import time
import asyncio


def start_slack():
    SocketModeHandler(app, slack_app_token).start()




def create_pair():
    
    g_id = db.get_all_groupid()
    if bool(g_id) == True:
        for i in g_id:
            dict_of_pair, arr_of_interest, platform = db.update_value_of_relatioships(i)
            print(platform)
            for ind, u1 in enumerate(dict_of_pair):
                if platfrom == 'tg':
                    telegramClient.send_pair(i, u1, dict_of_pair[u1], arr_of_interest[ind])
                elif platfrom == 'slack':
                    send_pair(i, u1, dict_of_pair[u1], arr_of_interest[ind])





schedule.every().day.at("13:20").do(create_pair)

def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)
 

if __name__ == "__main__":
    thread1 = Thread(target=start_slack, args=(), daemon=True)
    thread2 = Thread(target=loop, args=(), daemon=True)
    thread1.start()
    thread2.start()
    telegramClient.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates = True)


