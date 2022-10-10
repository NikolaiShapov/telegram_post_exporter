from getpass import getpass #Что-то типа input, но не выводит, что пишет пользователь (пароль)
import sys #Модуль со взаимодействием с системными функциями, будем исп sys.exit для верного завершение скрипта (без return)

from webapp import create_app
from webapp.model_my import User, db

app = create_app()

#Создаем пользователя
with app.app_context(): #Стала доступна работа с БД
    username = input('Введите имя пользователя: ') # Создаем апликейшен и создаем имя пользователя

    if User.query.filter(User.username == username).count(): #Проверка пользователя с именем (что существует)
        print('Пользователь с таким именем существует')
        sys.exit(0) #Выходим из нашей программы

    
    password = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password == password2:
        print('Пароли не схожи')
        sys.exit(0)
    
    #Если проверки пройдены, создаем пользователя
    new_user = User(username=username, role='admin') # Можно role переделать и запрашивать роль, проверять юзер или админ/ while
    new_user.set_password(password) # Ставим пользователю пароль в виде измененного хэша

    db.session.add(new_user)
    db.session.commit()

    print('Создан пользователь с id={}'.format(new_user.id))