from webapp import create_app
from webapp.tg_def import parser_post_channel, add_channel, add_user_channel, del_user_channel
# from webapp.tg_def_user_channel import add_channel

app = create_app()

with app.app_context():
    # parser_post_channel((1378813139,))
    # print(add_channel('https://t.me/bazabazon'))
    # print(add_channel('https://t.me/itubernews'))
    # channel_id_db = add_channel('https://t.me/codeby_sec')

    channel_id_db = add_channel('https://t.me/bazabazon')
    # print(add_user_channel(2, channel_id_db))

    # del_user_channel(2, 'https://t.me/bazabazon')
