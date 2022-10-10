from flask import Flask, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import LoginManager, login_required, current_user, login_user, logout_user #LoginManager - главный объект во flask_login, занимается менеджемнетом всего процесса логина
    #login_required - декоратор (Создадим страницу, доступную только зарегистрированным)


from webapp.forms_my import LoginForm
from webapp.model_my import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader #Получаем по id нужного пользователя через запрос к БД
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = app.config['TEST_KEY']
        first_text = "Hello, project"
        return render_template('index_my.html', 
                                page_title=title, 
                                first=first_text
                            )
    

    @app.route('/login')
    def login():
        print(current_user)
        if current_user.is_authenticated: 
            return redirect(url_for('index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
        title = "Авторизация"
        login_form = LoginForm() # Создался экземпляр логина
        return render_template('login_my.html', page_title=title, form=login_form)


    @app.route('/process-login', methods = ['POST']) #По умолчанию route обрабатывает только метод get. Мы хотим только метод POST
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user) #Запоминаем пользователя, если успешно вошел на сайт
                flash('Вы успешно вошли на сайт') #Создали сообщение
                return redirect(url_for('index')) #Переадресовали на главную страницу

        flash('Неправильное имя или пароль')
        return redirect(url_for('login'))


    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))


    @app.route('/admin')
    @login_required #Если пользователь не аутентифицирован, то перебрасывает на логин.
    def admin_index():
        if current_user.is_admin:
            return 'Hi, admin.'
        else:
            return 'You are not a admin'
            

    return app