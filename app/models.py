from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)

    tasks = db.relationship('Task', backref='user', lazy=True)

    profile_image = db.Column(db.String(150), nullable=False, default='default_image.png')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='未完了')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 新しいカラム
    order = db.Column(db.Integer, default=0)  # 順序を表す新しいフィールド

    def __repr__(self):
        return f'<Task {self.title}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

# User モデルにカテゴリリレーションを追加
User.categories = db.relationship('Category', backref='user', lazy=True)

 