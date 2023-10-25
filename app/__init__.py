from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # Flask-LoginのLoginManagerをインポート
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object('config')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()  # LoginManagerのインスタンスを作成
login_manager.init_app(app)  # LoginManagerをFlaskアプリに関連付け
login_manager.login_view = "login"  # ログインページへのリダイレクトのためのエンドポイント名
login_manager.login_message = "このページにアクセスするにはログインが必要です。"  # ログインメッセージのカスタマイズ

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

from app import routes

 

