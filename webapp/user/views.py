from flask import Blueprint, current_app, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import current_user, login_user, logout_user

from flask import send_file
from tg_downloan import create_report_posts, get_list_show_tg_channel_username
from tg_search import find
from webapp import db
from webapp.user.forms import LoginForm, RegistrationForm, AddChannel
from webapp.user.models import User, Channel, Post, User_channel
from subprocess import check_output
import os

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/user_ch')
def user_ch():
    title = "Личный кабинет."
    form = AddChannel()
    print(f'user = {current_user}')
    your_channels = get_list_show_tg_channel_username(f'{current_user.id}')
    your_channels.sort()

    return render_template('user/user.html', first=title, form=form, your_с=your_channels)

@blueprint.route('/process-add-ch', methods=['POST'])
def process_add_ch():
    form = AddChannel()
    if form.validate_on_submit():
        if form.submit_download_txt.data:
            try:
                filename = create_report_posts(f'{current_user.id}', f'{form.day_count.data}')
                print(filename)
                safe_path = os.path.join(current_app.config["FOLDER_DOWNLOAD"], filename)
                print(f'Отправляем файл {safe_path}')
                return send_file(safe_path, as_attachment=True, mimetype='text/csv')
            except:
                flash(f'Ошибка! Скачать не удалось!')
                return redirect(url_for('user.user_ch')) 
        if form.submit_search.data:
            try:
                if form.search.data == '':
                    raise ('Пуйсто запрос')
                # 1. запросить группы на которые подписан
                # 2. собирет все посты этих групп с проверкой искомого слова(фразы)
                # 3. создать файл
                # 4. Вывести информацию сколько постов найдено
                # 5. Вывести скнопку скачать
                # filename = create_report_posts(f'{current_user.id}', f'{form.day_count.data}')
                # print(filename)
                # safe_path = os.path.join(current_app.config["FOLDER_DOWNLOAD"], filename)
                # print(f'Отправляем файл {safe_path}')
                # return send_file(safe_path, as_attachment=True, mimetype='text/csv')
            except:
                flash(f'Ошибка! Поля не заполнены либо что то еще ...!')
                return redirect(url_for('user.user_ch')) 

        try:
            if form.submit_add.data:
                status_command = check_output(f'python tg_tasks.py {current_user.id} {form.url_channel.data} add_channel'.split(), encoding = 'utf-8')
            elif form.submit_del.data:
                status_command = check_output(f'python tg_tasks.py {current_user.id} {form.url_channel.data} del_user_channel'.split(), encoding = 'utf-8')
            print(f'status_command: {status_command}')
            status_command = status_command.strip().split('\n')[-1]
            flash(f'Статус: {status_command}!')
            return redirect(url_for('user.user_ch'))
        except:
            flash(f'Ошибка! Введено некорректное название Канала!')
            return redirect(url_for('user.user_ch'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.user_ch'))



@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
    page = "Авторизация"
    form = LoginForm() # Создался экземпляр логина
    return render_template('user/login.html', first=page, form=form)


@blueprint.route('/process-login', methods = ['POST']) #По умолчанию route обрабатывает только метод get. Мы хотим только метод POST
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data) #Запоминаем пользователя, если успешно вошел на сайт
            flash('Вы успешно вошли на сайт') #Создали сообщение
            return redirect(url_for('news.index')) #Переадресовали на главную страницу

    flash('Неправильное имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    page = "Регистрация"
    form = RegistrationForm()
    return render_template('user/registration.html', first=page, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.register'))