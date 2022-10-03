#для создания сессии
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

#
from sqlalchemy import Column, Integer, String, Date, Text, BIGINT, Boolean

engine = create_engine('postgresql://postgres:123456@127.0.0.1/bd_test')
db_session = scoped_session(sessionmaker(bind=engine)) # Создали ссеию
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    mail = Column(String, unique=True, nullable=False) #unique - уникальность #nullable=False - данное значение обязательно должно быть
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.mail}, {self.password}'

class channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True)
    tg_channel_id = Column(BIGINT, nullable=False)
    tg_channel_title = Column(String, nullable=False)
    tg_channel_username = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.tg_channel_id}, {self.tg_channel_title}'

class post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    channel_id = Column(BIGINT, nullable=False)
    tg_post_id = Column(BIGINT, nullable=False)
    tg_participants_count = Column(Integer, nullable=False)
    tg_data_post = Column(Date, nullable=False)
    tg_text_post = Column(Text, nullable=False)
    img_flag = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.channel_id}, {self.tg_post_id}, {self.tg_text_post}'

class user_channel(Base):
    __tablename__ = "user_channels"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    is_delete = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.user_id}, {self.channel_id}'

class keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    keyword = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.user_id}, {self.keyword}'

class keyword_post(Base):
    __tablename__ = "keyword_posts"
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.keyword_id}, {self.post_id}'

class img(Base):
    __tablename__ = "imgs"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    img_path = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'News {self.post_id}, {self.img_path}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
