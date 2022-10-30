from flask_login import UserMixin #Добавим в нашу модель интеграцию с Flask-Login. Мы можем создать эти поля и метод руками, но можно поступить проще и использовать UserMixin.
from werkzeug.security import generate_password_hash, check_password_hash #Работа с паролем, шифруем его без воз-ти расшифровки

from webapp import db

class User(db.Model, UserMixin): #Модель пользователя
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True) #Роль людей (админ или юзер)
    email = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password) #Шифровка пароля ч/з generate_password_hash. В БД идет шифровка.

    def check_password(self, password):
        return check_password_hash(self.password, password) #Возвращает True или False (через шифровку, а не оригинал)

    @property
    def is_admin(self):
        return self.role == 'admin' #Декоратор @property позволяет вызывать метод как атрибут, без скобочек. Проверка на админа

    def __repr__(self):
        return '<User name = {} id = {}>'.format(self.username, self.id) #Получаем строчку

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
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True, nullable=False)
    # user_id = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey(Channel.id), index=True, nullable=False)
    # channel_id = db.Column(db.Integer, nullable=False)
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