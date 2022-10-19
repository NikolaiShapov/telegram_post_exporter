from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

TEST_KEY = "Final Project LearnPython"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
PATH_IMG = os.path.join(basedir, '..', 'img_root')

SECRET_KEY = "safsgw4ewefdsge563424rewrhge5634"

REMEMBER_COOKIE_DURATION = timedelta(days=5)

#Это отключит функционал отправки сигнала приложению при изменениях в БД - мы не будем пользоваться им, 
# т.к. он создает большую дополнительную нагрузку на приложение.
SQLALCHEMY_TRACK_MODIFICATIONS = False
