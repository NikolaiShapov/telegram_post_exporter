from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.patched import MessageService
from webapp.config import PATH_IMG
from webapp.settings import API_HASH, API_ID
from tg_db import db_session
from tg_models import Post, Img, User, User_channel, Channel
import datetime, time
import os

def participants_count_Channel(id_Channel):
    full_info = client(functions.channels.GetFullChannelRequest(channel=int(f'-100{id_Channel}')))
    return(full_info.full_chat.participants_count) # количество подписчиков канала

def parser_post_channel(list_id_Channel):
    for id in list_id_Channel:
        messages = []
        grouped_id = []
        channel = client.get_entity(int(f'-100{id}')) # получаем канал по ID (к id канала надо дописать -100)
        tg_participants_count = participants_count_Channel(id)
        for message in client.iter_messages(channel,limit=30):
            # print(message.stringify())
            if len(grouped_id) > 0 and isinstance(message, MessageService):
                loader_posts(messages, tg_participants_count, id)
                messages = []
                grouped_id = []
                continue
            if len(grouped_id) == 0 and isinstance(message, MessageService):
                continue
            if not message.grouped_id is None: #обрабатываем составные посты
                if len(grouped_id) == False:
                    grouped_id.append(message.grouped_id)
                    messages.append(message)
                    continue
                else:
                    if message.grouped_id in grouped_id:
                        grouped_id.append(message.grouped_id)
                        messages.append(message)
                        continue
                    else:
                        loader_posts(messages, tg_participants_count, id)
                        messages = []
                        grouped_id = []
                        messages.append(message)
                        grouped_id.append(message.grouped_id)
                        continue
            elif len(grouped_id) > 0:
                loader_posts(messages, tg_participants_count, id)
                messages = []
                grouped_id = []
            if message.grouped_id is None: #обрабатываем "простые" посты
                loader_post(message, tg_participants_count, id)

def loader_post(message, tg_participants_count, id):
    double = Post.query.filter(Post.tg_post_id==message.id, Post.channel_id==id).count()
    if double == 0:
        img_flag = False
        try:
            if not message.media.photo is None:
                img_flag = True
                path_photo = os.path.join(PATH_IMG, str(id), str(message.id), str(message.media.photo.id) + '.jpg')
                client.download_media(message, file = path_photo)
        except AttributeError:
            if message.text == "":
                return 'Это добавлять в БД не будем.'
        new_post = create_new_post_one(id, message, tg_participants_count, img_flag)
        loader_post_db(new_post)
        if img_flag == True:
            new_img = Img(post_id = new_post.id, img_path = os.path.join(PATH_IMG, str(id), str(message.id)))
            loader_img_db(new_img)
        else:
            db_session.commit()

def create_new_post_one(id, message, tg_participants_count, img_flag):
    new_post =Post(
            channel_id = id,
            tg_post_id = message.id,
            tg_data_post = message.date.replace(tzinfo=None) + datetime.timedelta(hours=3), # Московское время,
            tg_text_post = message.text,
            tg_participants_count = tg_participants_count,
            img_flag = img_flag)
    return new_post

def create_new_post_all(id, messages, tg_participants_count, img_flag):
    #Практика показала, что тест поста не всегдна храниться в последнем элемента ВСЕГО поста.
    #По этому собираем текст по всем элемента поста
    texts = ''
    for mess in messages:
        texts += mess.text
    new_post =Post(
            channel_id = id,
            tg_post_id = messages[-1].id,
            tg_data_post = messages[-1].date.replace(tzinfo=None) + datetime.timedelta(hours=3), # Московское время,
            tg_text_post = texts,
            tg_participants_count = tg_participants_count,
            img_flag = img_flag
            )
    return new_post

def loader_posts(messages, tg_participants_count, id):
    double = Post.query.filter((Post.tg_post_id==messages[-1].id and Post.channel_id==id)).count()
    if double == 0:
        for mess in messages:
            try:
                if not mess.media.photo is None:
                    path_photo = os.path.join(PATH_IMG, str(id), str(messages[-1].id), str(mess.media.photo.id) + '.jpg')
                    client.download_media(mess, file = path_photo)
            except AttributeError:
                pass
            if os.path.exists(os.path.join(PATH_IMG, str(id), str(messages[-1].id))):
                img_flag = True
            else:
                img_flag = False
        new_post = create_new_post_all(id, messages, tg_participants_count, img_flag)
        loader_post_db(new_post)
        if img_flag == True:
            new_img = Img(post_id = new_post.id, img_path = os.path.join(PATH_IMG, str(id), str(messages[-1].id)))
            loader_img_db(new_img)
        else:
            db_session.commit()

def loader_post_db(new_post):
    db_session.add(new_post)
    db_session.flush()
    print('+1')

def loader_img_db(new_img):
    db_session.add(new_img)
    db_session.commit()

if __name__ == '__main__':
    client = TelegramClient('+79811447016', API_ID, API_HASH)
    client.start()

    # Запросы к БД передать список ID
    parser_post_channel((1378813139,))
    # Как запускать (каждые 5 минут)? cron
    
