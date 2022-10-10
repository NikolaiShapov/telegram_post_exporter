from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #Типы полей, позволит создать поля для ввода пароля и сабмит
from wtforms.validators import DataRequired #Валидатор помогает избежать ручные проверки, проверяет, действительно ли пользователь ввел в поле

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"}) #render_kw - добавка к полю при рендеринге
    #1 - Лейбл, 2 - можно сделать так: validators=[DataRequired()] и имейл валидатор
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class":"btn btn-primary"})