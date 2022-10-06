from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.mail}, {self.password}'

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    tg_channel_id = db.Column(db.BIGINT, nullable=False)
    tg_channel_title = db.Column(db.String, nullable=False)
    tg_channel_username =db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.tg_channel_id}, {self.tg_channel_title}'

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.BIGINT, nullable=False)
    tg_post_id = db.Column(db.BIGINT, nullable=False)
    tg_participants_count = db.Column(db.Integer, nullable=False)
    tg_data_post = db.Column(db.Date, nullable=False)
    tg_text_post = db.Column(db.Text, nullable=False)
    img_flag = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.channel_id}, {self.tg_post_id}, {self.tg_text_post}'

class User_channel(db.Model):
    __tablename__ = "user_channels"
    id =db. Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.Integer, nullable=False)
    is_delete = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.user_id}, {self.channel_id}'

class Keyword(db.Model):
    __tablename__ = "keywords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    keyword = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.user_id}, {self.keyword}'

class Keyword_post(db.Model):
    __tablename__ = "keyword_posts"
    id = db.Column(db.Integer, primary_key=True)
    keyword_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.keyword_id}, {self.post_id}'

class Img(db.Model):
    __tablename__ = "imgs"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    img_path = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.post_id}, {self.img_path}'
