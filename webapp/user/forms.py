from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField #Типы полей, позволит создать поля для ввода пароля и сабмит
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError #Валидатор помогает избежать ручные проверки, проверяет, действительно ли пользователь ввел в поле

from webapp.user.models import User


class AddChannel(FlaskForm):
    url_channel = StringField('Введите название канала:', render_kw={"class": "form-control form-control-lg", "placeholder": "https://t.me/bazabazon"})
    submit_add = SubmitField('Добавить!', render_kw={"class":"btn btn-primary btn-lg btn-block"})
    submit_del = SubmitField('Удалить!', render_kw={"class":"btn btn-danger btn-lg btn-block"})
    day_count = StringField('Введите количество дней:', render_kw={"class": "form-control form-control-lg", "placeholder": "За сколько дней?"})
    submit_download_txt = SubmitField('Скачать Txt', render_kw={"class": "btn btn-success btn-lg btn-block"})
    submit_download_csv = SubmitField('Скачать Csv', render_kw={"class": "btn btn-secondary btn-lg btn-block"})
    submit_download_pdf = SubmitField('Скачать Pdf', render_kw={"class": "btn btn-warning btn-lg btn-block"})
    search = StringField('Поиск в базе постов:', render_kw={"class": "form-control form-control-lg", "placeholder": "Ваш запрос"})
    search_day = StringField('Поиск в базе постов:', render_kw={"class": "form-control form-control-lg", "placeholder": "За сколько дней?"})
    submit_search = SubmitField('Поиск', render_kw={"class": "btn btn-secondary btn-lg btn-block"})


# class Download(FlaskForm):
#     submit_download = StringField('Название канала', render_kw={"class": "btn btn-success btn-lg"})

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"}) #render_kw - добавка к полю при рендеринге
    #1 - Лейбл, 2 - можно сделать так: validators=[DataRequired()] и имейл валидатор
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"}) # default=True - галочка запомнить стоит по умолчанию
    submit = SubmitField('Отправить!', render_kw={"class":"btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')