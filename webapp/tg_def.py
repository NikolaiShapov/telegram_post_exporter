from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.patched import MessageService
from webapp.config import PATH_IMG
from webapp.settings import API_HASH, API_ID
from webapp.user.models import db, Post, Img, User, User_channel, Channel
import datetime, time
import os

def client():
    client = TelegramClient('+79811447016', API_ID, API_HASH)
    return client.start()

def add_channel(url_channel):
    print(url_channel)
    channel = client().get_entity(url_channel)
    double_channel = Channel.query.filter(Channel.tg_channel_id==channel.id).count()
    if double_channel == 0:
        new_add_channel =Channel(
            tg_channel_id = channel.id,
            tg_channel_title = channel.title,
            tg_channel_username = channel.username
            )
        db.add(new_add_channel)#, return_defaults=True)
        db.commit()
        return new_add_channel.id #"Add сhannel!"
    else:
        return get_channel_id_bd(channel.id) #"Сhannel already exists!"

def get_channel_id_bd(channel_id):
    channel_id_bd = db.session.query(Channel).filter(Channel.tg_channel_id==channel_id).first()
    return channel_id_bd.id

def get_user_id_bd(user_email):
    user_id_bd = db.session.query(User).filter(User.email==user_email).first()
    return user_id_bd.id

def is_channel_db_user(user_id, channel_id):
    is_user_channel = db.session.query(User_channel).filter(User_channel.user_id==user_id, User_channel.channel_id == channel_id).count()
    if is_user_channel == 0:
        return True
    else:
        False

def max_channel_user(user_id):
    count_user_channel = db.session.query(User_channel).filter(User_channel.user_id==user_id, User_channel.is_delete == True).all()
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
            db.session.add(new_user_channel)
            db.session.commit()
            return 'канал добавлен'
        else:
            return 'Max Channel 20!'
    else:
        return update_del_true(user_id, channel_id)

def update_del_true(user_id, channel_id):
    update_del = db.session.query(User_channel).filter(User_channel.user_id==user_id, User_channel.channel_id == channel_id).first()
    print(update_del.is_delete)
    if update_del.is_delete:
        return 'Уже есть в списке'
    else:
        update_del.is_delete = True
        db.session.add(update_del)
        db.session.commit()
        return 'Восстановили!'


def del_user_channel(user_id, url_channel):
    channel = client.get_entity(url_channel)
    id_db_channel = get_channel_id_bd(channel.id)
    update_del = db.session.query(User_channel).filter(User_channel.user_id==user_id, User_channel.channel_id == id_db_channel).first()
    update_del.is_delete = False
    db.session.add(update_del)
    db.session.commit()

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
    double = db.session.query(Post).filter(Post.tg_post_id==message.id, Post.channel_id==id).count()
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
            db.session.commit()

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
    double = db.session.query(Post).filter((Post.tg_post_id==messages[-1].id and Post.channel_id==id)).count()
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
            db.session.commit()

def loader_post_db(new_post):
    db.session.add(new_post)
    db.session.flush()
    print('+1')

def loader_img_db(new_img):
    db.session.add(new_img)
    db.session.commit()


if __name__ == "__main__":
    # posts = parser_post_channel((1378813139,))
    # channel_id_db = add_channel('https://t.me/bazabazon')
    # print(add_user_channel(2, channel_id_db))
    pass
