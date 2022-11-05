from tg_txt import get_list_user_channel, get_dict_channel
from tg_models import Post
import datetime

def get_user_post(list_tg_id_channel, day, search):
    print(list_tg_id_channel)
    day = datetime.date.today() - datetime.timedelta(days=int(day)-1)
    print(f'Собираем посты с даты: {day}')
    db_post = Post.query.filter(Post.channel_id.in_(list_tg_id_channel),
                                Post.tg_data_post >= day,
                                Post.tg_text_post.ilike("%{search}%")).order_by(Post.channel_id).order_by(Post.tg_data_post).all()
    print(len(db_post))
    print(db_post)
    return db_post

def find(user_id, search,search_day):
    list_user_channel = get_list_user_channel(user_id)
    dict_channel = get_dict_channel(list_user_channel)
    posts = get_user_post(list(map(int, dict_channel)), search_day, search)

if __name__ == '__main__':
    find(5,'США',12)

