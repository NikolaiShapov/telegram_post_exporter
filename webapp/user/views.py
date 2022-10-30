from flask import Blueprint, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import current_user, login_user, logout_user

from webapp import db
from webapp.user.forms import LoginForm, RegistrationForm, AddChannel
from webapp.user.models import User
from webapp.tg_def import parser_post_channel, add_channel, add_user_channel, del_user_channel

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
    title = "Авторизация"
    login_form = LoginForm() # Создался экземпляр логина
    return render_template('user/login.html', page_title=title, form=login_form)



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




@blueprint.route('/user_ch')
def user_ch():
    title = "Приветик, красавчик"
    form = AddChannel()
    return render_template('user./user.html', first=title, form=form)



@blueprint.route('/process-add-ch', methods=['POST'])
def process_add_ch():
    form = AddChannel()
    if form.validate_on_submit():
        channel_id_db = add_channel(form.url_channel.data) # Необходима проверка корректности ввода данных названия канала
        flash(f'Добавляем канал {channel_id_db}!')
        return redirect(url_for('user.user_ch'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.user_ch'))




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