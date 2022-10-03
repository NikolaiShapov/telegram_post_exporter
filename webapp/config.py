import os
basedir = os.path.abspath(os.path.dirname(__file__)) #получаем полный путь до файла __file__, который и есть config.py

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
