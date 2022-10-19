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