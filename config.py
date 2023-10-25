import os
from flask_uploads import IMAGES

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'your_secret_key_here'
 
UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, 'app/static/uploads')
UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, 'app/static/uploads/photos')
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MBのサイズ制限
UPLOADED_PHOTOS_ALLOW = IMAGES