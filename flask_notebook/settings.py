import os
from flask_notebook import app


prefix ='sqlite:///'
flag = '?check_same_thread=False'
filename ='data.db'
dev_db = (prefix + os.path.join(os.path.dirname(app.root_path), filename)) + flag


# some settings
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
