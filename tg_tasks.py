from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.patched import MessageService
from webapp.config import PATH_IMG
from webapp.settings import API_HASH, API_ID
from tg_models import Post, Img, User, User_channel, Channel
from tg_db import db_session
import sys

def add_channel(url_channel):
    print(url_channel)
    channel = client.get_entity(url_channel)
    if channel.megagroup:
        print('Можно добавлять только Каналы!')
        return 'Можно добавлять только Каналы!'
    print('db run...')
    double_channel = Channel.query.filter(Channel.tg_channel_id==channel.id).count()
    if double_channel == 0:
        new_add_channel =Channel(
            tg_channel_id = channel.id,
            tg_channel_title = channel.title,
            tg_channel_username = channel.username
            )
        db_session.add(new_add_channel)#, return_defaults=True)
        db_session.commit()
        print(channel.id, channel.title, channel.username)
        add_channel_in_telegram(channel.username)
        return new_add_channel.id #"Add сhannel!"
    else:
        return get_channel_id_bd(channel.id) #"Сhannel already exists!"

def get_channel_id_bd(channel_id):
    channel_id_bd = Channel.query.filter(Channel.tg_channel_id==channel_id).first()
    return channel_id_bd.id

def get_user_id_bd(user_email):
    user_id_bd = User.query.filter(User.email==user_email).first()
    return user_id_bd.id

def add_channel_in_telegram(username):
    client(JoinChannelRequest(username))
    print(f'JoinChannelRequest:{username}')

def is_channel_db_user(user_id, channel_id):
    is_user_channel = User_channel.query.filter(User_channel.user_id==user_id, User_channel.channel_id == channel_id).count()
    if is_user_channel == 0:
        return True
    else:
        False

def max_channel_user(user_id):
    count_user_channel = User_channel.query.filter(User_channel.user_id==user_id, User_channel.is_delete == True).all()
    if len(count_user_channel) < 20:
        return True
    else:
        return False

def add_user_channel(user_id, channel_id):
    if is_channel_db_user(user_id, channel_id):
        if max_channel_user(user_id):
            new_user_channel = User_channel(
                    user_id = user_id,
                    channel_id = channel_id,
                    is_delete = True
                    )
            db_session.add(new_user_channel)
            db_session.commit()
            return 'канал добавлен'
        else:
            return 'Max Channel 20!'
    else:
        return update_del_true(user_id, channel_id)

def update_del_true(user_id, channel_id):
    update_del = User_channel.query.filter(User_channel.user_id==user_id, User_channel.channel_id == channel_id).first()
    print(update_del.is_delete)
    if update_del.is_delete:
        return 'Уже есть в списке'
    else:
        update_del.is_delete = True
        db_session.add(update_del)
        db_session.commit()
        return 'Восстановили!'


def del_user_channel(user_id, url_channel):
    channel = client.get_entity(url_channel)
    id_db_channel = get_channel_id_bd(channel.id)
    update_del = User_channel.query.filter(User_channel.user_id==user_id, User_channel.channel_id == id_db_channel).first()
    update_del.is_delete = False
    db_session.add(update_del)
    db_session.commit()
    return 'Канал удален!'

if __name__ == "__main__":
    client = TelegramClient('+79811447016', API_ID, API_HASH)
    client.start()

    print(sys.argv)
    command = sys.argv[-1]
    channels = sys.argv[-2]
    id_user = sys.argv[-3]
    print(f'command: {command}')

    if command == 'add_channel':
        #Нужна проверка что это именно группа!
        channel_id_db = add_channel(channels)
        if type(channel_id_db) is int:
            print('Добавляем канал...')
            result = add_user_channel(id_user, channel_id_db)
            print(result)
    elif command == 'del_user_channel':
        result = del_user_channel(id_user, channels)
        print(result)
    else:
        print('Error command!')



