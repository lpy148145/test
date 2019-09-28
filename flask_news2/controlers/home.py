from flask import Blueprint, render_template
from modules import News

home_route = Blueprint('index', __name__)


@home_route.route('/')
def home():
    news_list = News.query.filter_by(is_valid=1).all()
    return render_template('home/index.html', news_list=news_list)


@home_route.route('/detail/<int:pk>')
def detail(pk):
    news_list = News.query.filter_by(is_valid=1, id=pk).all()
    return render_template('home/detail.html', news_list=news_list)


@home_route.route('/cat/<name>')
def cat(name):
    news_list = News.query.filter_by(is_valid=1, types=name).all()
    return render_template('home/cat.html', news_list=news_list)
