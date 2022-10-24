from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.patched import MessageService
from webapp.settings import API_HASH, API_ID
from webapp.user.models import db, User, User_channel, Channel
import datetime, time
import os


client = TelegramClient('+79811447016', API_ID, API_HASH)
client.start()

def add_channel(url_channel):
    channel = client.get_entity(url_channel)
    print(channel)

def del_channel():
    pass

def is_channel_db_user():
    pass

def max_channel_user():
    pass


def loader_post_db(new_post):
    db.session.add(new_post)
    db.session.flush()
    print('+1')

def loader_img_db(new_img):
    db.session.add(new_img)
    db.session.commit()


if __name__ == "__main__":
    add_channel('https://t.me/bazabazon')
    # posts = parser_post_channel((1378813139,))
