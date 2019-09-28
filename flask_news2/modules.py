from werkzeug.security import generate_password_hash
from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    is_valid = db.Column(db.Boolean, default=True)

    def __init__(self, username, password, is_valid):
        self.username = username
        self.password = generate_password_hash(password)
        self.is_valid = is_valid


class News(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    img_url = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=1)
    is_recommend = db.Column(db.Boolean, default=0)

    def __init__(self, title, content, types, img_url, author, view_count, created_at, is_valid, is_recommend):
        self.title = title
        self.content = content
        self.types = types
        self.img_url = img_url
        self.author = author
        self.view_count = view_count
        self.created_at = created_at
        self.is_valid = is_valid
        self.is_recommend = is_recommend

