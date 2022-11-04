from flask import Blueprint, render_template, current_app
from webapp.user.models import User, Channel, Post

blueprint = Blueprint('news', __name__)

@blueprint.route("/")
def index():
    title = current_app.config['TEST_KEY']
    first_text = "Проект Telegram post exporter"
    count_User = User.query.order_by(User.username).count()
    count_Channel = Channel.query.order_by(Channel.tg_channel_id).count()
    count_Post = Post.query.order_by(Post.id).count()
    return render_template('news/index.html', 
                            page_title=title, 
                            first=first_text,
                            users=count_User,
                            channels=count_Channel,
                            posts=count_Post
                        )
        