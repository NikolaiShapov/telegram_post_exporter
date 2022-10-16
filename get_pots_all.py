from webapp import create_app
from webapp.tg_def import parser_post_channel

app = create_app()

with app.app_context():
    parser_post_channel((1378813139,))
