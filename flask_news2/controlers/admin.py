from flask import Blueprint, render_template, url_for, flash, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import UserForm, NewsForm
from functools import wraps
from application import db
from modules import User, News
from datetime import datetime


admin = Blueprint('admin', __name__)


# 定义一个实现访问控制的装饰器 admin_login_require
def admin_login_require(f):
    # 使用functools.wraps装饰器装饰内函数wrapper，从而可以保留被修饰的函数属性
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断是否登录
        if 'userid' not in session:
            # 如果session中没有userid的键名，则重定向到登录页
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_valid=1).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['userid'] = user.id
            return redirect(url_for('admin.index'))
        else:
            flash("您输入的用户名或密码错误", category='error')
    return render_template('admin/login.html')


@admin.route('/')
@admin_login_require
def index():
    return render_template('admin/index.html')

# 退出
@admin.route('/logout')
# @admin_login_require
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route('/changePassword', methods=['GET', 'POST'])
@admin_login_require
def changePassword():
    print(session['username'],session['userid'])
    _id = session['userid']
    user1 = User.query.get(_id)
    form = UserForm(obj=user1)

    if form.validate_on_submit():
        user1.password = generate_password_hash(form.password.data)
        db.session.add(user1)
        db.session.commit()
        flash('修改密码成功! 请重新登录')
        return redirect(url_for('admin.login'))
    return render_template('admin/changePassword.html', form=form)


@admin.errorhandler(404)
def get_error(error):
    return render_template('admin/error.html'), 404


@admin.route('/user/')
@admin.route('/user/<int:page>')
@admin_login_require
def manager_user(page=None):

    # 分页查询
    if page is None:
        page = 1
    # 接收查询的值
    keyword = request.args.get('search')
    if keyword:
        try:
            user_list = User.query.filter(User.username.contains(keyword)).\
                order_by(User.id).\
                paginate(page=page, per_page=2)
            condition = "?search=" + keyword
            return render_template('admin/user_index.html', user_list=user_list, condition=condition)
        except:
            flash('搜索失败！')
    else:
        user_list = User.query.paginate(page=page, per_page=5)
        return render_template('admin/user_index.html', user_list=user_list)


@admin.route('/user/add', methods=['GET', 'POST'])
@admin_login_require
def user_add():

    form = UserForm()
    # print(form.__dict__)
    # 判断表单是否通过
    try:
        if form.validate_on_submit():
            user = User(form.username.data,
                        form.password.data,
                        form.is_valid.data)
            db.session.add(user)
            db.session.commit()
            flash('添加成功!')
            return redirect(url_for('admin.manager_user'))
    except:
        flash('你输入的用户名已存在!', category='error')
    return render_template('admin/user_add.html', form=form)


@admin.route('/user/delete/<int:_id>')
@admin_login_require
def delete_user(_id=None):

    try:
        user = User.query.get(_id)
        db.session.delete(user)
        db.session.commit()
        flash('删除成功!')
        return redirect(url_for('admin.manager_user'))
    except:
        flash('删除失败!', category='error')


@admin.route('/user/update/<int:_id>', methods=['GET', 'POST'])
@admin_login_require
def update_user(_id):

    user = User.query.get(_id)
    if user is None:
        return redirect(url_for('admin.manager_user'))
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.is_valid = form.is_valid.data
            db.session.add(user)
            db.session.commit()
            flash('成功修改管理员')
        except:
            flash('您输入的用户名已存在!', category='error')
    return render_template('admin/user_update.html', form=form)


@admin.route('/detail')
@admin_login_require
def news_detail():
    news_list = News.query.all()
    return render_template('admin/news_detail.html', news_list=news_list)


@admin.route('/detail/add', methods=['GET', 'POST'])
@admin_login_require
def news_add():
    form = NewsForm()
    form.created_at.data = datetime.now()
    try:
        if form.validate_on_submit():
            news = News(form.title.data,
                        form.content.data,
                        form.types.data,
                        form.img_url.data,
                        form.author.data,
                        form.view_count.data,
                        form.created_at.data,
                        form.is_valid.data,
                        form.is_recommend.data)
            db.session.add(news)
            db.session.commit()
            flash('添加新闻成功!')
            return redirect(url_for('admin.news_detail'))
    except:
        flash('添加新闻失败!', category='error')
    return render_template('admin/news_add.html', form=form)
