from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.secret_key = 'this is a key'
# 连接mysql数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hao@123@192.168.208.136/news?charset=utf8mb4'
db = SQLAlchemy(app)


