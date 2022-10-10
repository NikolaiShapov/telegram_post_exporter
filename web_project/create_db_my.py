#QLAlchemy сама создаст файл базы данных (если его еще нет) и соответствующие таблицы по нашему описанию. 

from webapp import db, create_app

app=create_app()
with app.app_context():
    db.create_all()