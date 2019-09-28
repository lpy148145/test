from application import app
# 1.引入蓝图文件
from controlers.admin import admin
from controlers.home import home_route

# 2. 注册蓝图文件
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(home_route, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
