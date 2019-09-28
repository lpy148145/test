from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, TimeField, \
    IntegerField, FileField
from wtforms.validators import DataRequired, EqualTo, Length


class UserForm(FlaskForm):
    username = StringField('管理员用户名',
                           validators=[DataRequired('请填写管理员用户名'), Length(5, 12, message='用户名必须在5-12位之间')],
                           render_kw={'class': 'form-control'})

    password = PasswordField('管理员密码',
                             validators=[DataRequired('请填写管理员密码'), Length(6, 8, message='密码必须在6-8位之间')],
                             render_kw={'class': 'form-control'})

    repassword = PasswordField('重复密码',
                               validators=[DataRequired('请填写重复密码'), EqualTo('password', '填写密码不一致')],
                               render_kw={'class': 'form-control'})

    is_valid = BooleanField('是否启用')

    submit = SubmitField('提交', render_kw={'class': 'btn btn-primary'})


class NewsForm(FlaskForm):
    title = StringField('新闻标题',
                        validators=[DataRequired('请填写新闻标题')],
                        render_kw={'class': 'form-control'})

    content = TextAreaField('新闻内容',
                            validators=[DataRequired('请填写新闻内容')],
                            render_kw={'class': 'form-control'})

    types = SelectField('新闻类型',
                        coerce=str,
                        validators=[DataRequired('请填写新闻类型')],
                        choices=[('娱乐', '娱乐'), ('科技', '科技')],
                        render_kw={'class': 'form-control'})

    img_url = StringField('图片地址',
                          validators=[DataRequired('请填写图片地址')],
                          render_kw={'class': 'form-control'})

    author = StringField('新闻作者',
                         validators=[DataRequired('请填写新闻作者')],
                         render_kw={'class': 'form-control'})

    view_count = IntegerField('观看数量',
                              validators=[DataRequired('请填写观看数量')],
                              render_kw={'class': 'form-control'})

    created_at = TimeField('上传时间',
                           validators=[DataRequired('请填写上传时间')],
                           render_kw={'class': 'form-control'})

    is_valid = BooleanField('是否上架')

    is_recommend = BooleanField('是否推荐')

    submit = SubmitField('提交', render_kw={'class': 'btn btn-primary'})
