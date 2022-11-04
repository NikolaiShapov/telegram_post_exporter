from tg_models import Post, User_channel, Channel
import sys
import datetime

def get_list_user_channel(id_user): #Берет id каналов на которые подписан пользователь
    list_temp = []
    for id_table_channel in User_channel.query.filter(User_channel.is_delete != 0, User_channel.user_id == id_user ).all():
        list_temp.append(id_table_channel.channel_id)
    return list_temp

def get_dict_channel(list_user_channel): #Создает словарь id_channel:channel_username
    dict_ch = {}
    db_channel = Channel.query.group_by(Channel.tg_channel_id).all()
    print(len(db_channel))
    for channel in db_channel:
        # print(channel.tg_channel_id, channel.tg_channel_username)
        if channel.id in list_user_channel:
            dict_ch[str(channel.tg_channel_id)] = channel.tg_channel_username
    return dict_ch

def get_user_post(list_tg_id_channel, day):
    print(list_tg_id_channel)
    print(f'Собираем посты с даты: {day}')
    db_post = Post.query.filter(Post.channel_id.in_(list_tg_id_channel), Post.tg_data_post >= day).order_by(Post.channel_id).order_by(Post.tg_data_post).all()
    print(len(db_post))
    return db_post

def creat_doc_txt(dict_channel, posts, day):
    DMY = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    with open('download/tg_post' + DMY + '.txt', 'w', encoding='utf-8') as file:
        file.writelines(f'Отчет постов с даты {day}.\n\n')
        for post in posts:
            file.writelines(f'название канала: {dict_channel[str(post.channel_id)]}\n')
            file.writelines(f'дата поста: {post.tg_data_post}\n')
            file.writelines(f'колличество подписчиков: {post.tg_participants_count}\n')
            file.writelines(post.tg_text_post + '\n')
            file.writelines('====\n')
    print('Файл сформирован!')
    print('tg_post' + DMY + '.txt')

if __name__ == "__main__":
    print(sys.argv)    
    day = sys.argv[-1]
    id_user = sys.argv[-2]
    day = datetime.date.today() - datetime.timedelta(days=int(day)-1)
    

    list_user_channel = get_list_user_channel(5)
    dict_channel = get_dict_channel(list_user_channel)
    posts = get_user_post(list(map(int, dict_channel)), day)
    creat_doc_txt(dict_channel, posts, day)