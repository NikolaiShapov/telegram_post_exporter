from tg_txt import get_list_user_channel, get_dict_channel
from tg_models import Post
import datetime

def get_user_post(list_tg_id_channel, day, search):
    print(list_tg_id_channel)
    print(f'Собираем посты с даты: {day}')
    print(search)
    db_post = Post.query.filter(Post.channel_id.in_(list_tg_id_channel),
                                Post.tg_data_post >= day,
                                Post.tg_text_post.ilike(f"%{search}%")).order_by(Post.channel_id).order_by(Post.tg_data_post).all()
    print(len(db_post))
    return db_post

def creat_search_doc_txt(dict_channel, posts, day, search):
    DMY = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    with open('download/tg_post_search' + DMY + '.txt', 'w', encoding='utf-8') as file:
        file.writelines(f'Отчет постов с даты {day}.\n')
        file.writelines(f'Ваш запрос: {search}.\n\n')
        for post in posts:
            file.writelines(f'название канала: {dict_channel[str(post.channel_id)]}\n')
            file.writelines(f'дата поста: {post.tg_data_post}\n')
            file.writelines(f'колличество подписчиков: {post.tg_participants_count}\n')
            file.writelines(post.tg_text_post + '\n')
            file.writelines('====\n')
    print('Файл сформирован!')
    print('tg_post_search' + DMY + '.txt')
    return 'tg_post_search' + DMY + '.txt'

def find(user_id, search,search_day):
    day = datetime.date.today() - datetime.timedelta(days=int(search_day)-1)
    list_user_channel = get_list_user_channel(user_id)
    dict_channel = get_dict_channel(list_user_channel)
    posts = get_user_post(list(map(int, dict_channel)), day, search)
    filename = creat_search_doc_txt(dict_channel, posts, day, search)
    return filename

if __name__ == '__main__':
    find(5,'США',2)

