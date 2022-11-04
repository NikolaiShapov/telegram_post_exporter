
from sqlalchemy import Column, Integer, String, Date, ForeignKey, BIGINT, Text, Boolean
from tg_db import Base, engine


class User(Base): #Модель пользователя
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    role = Column(String(10), index=True) #Роль людей (админ или юзер)
    email = Column(String(50))

    @property
    def is_admin(self):
        return self.role == 'admin' #Декоратор @property позволяет вызывать метод как атрибут, без скобочек. Проверка на админа

    def __repr__(self):
        return '<User name = {} id = {}>'.format(self.username, self.id) #Получаем строчку

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True)
    tg_channel_id = Column(BIGINT, nullable=False)
    tg_channel_title = Column(String, nullable=False)
    tg_channel_username =Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.tg_channel_id},{self.tg_channel_title}'

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    channel_id = Column(BIGINT, nullable=False)
    tg_post_id = Column(BIGINT, nullable=False)
    tg_participants_count = Column(Integer, nullable=False)
    tg_data_post = Column(Date, nullable=False)
    tg_text_post = Column(Text, nullable=False)
    img_flag = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'{self.channel_id},{self.tg_post_id},{self.tg_text_post}'

class User_channel(Base):
    __tablename__ = "user_channels"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    # user_id = Column(Integer, nullable=False)
    channel_id = Column(Integer, ForeignKey(Channel.id), index=True, nullable=False)
    # channel_id = Column(Integer, nullable=False)
    is_delete = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'{self.user_id},{self.channel_id}'

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    keyword = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.user_id},{self.keyword}'

class Keyword_post(Base):
    __tablename__ = "keyword_posts"
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'{self.keyword_id},{self.post_id}'

class Img(Base):
    __tablename__ = "imgs"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    img_path = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.post_id},{self.img_path}'