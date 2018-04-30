from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = '/app/static/img'
login = LoginManager(app)
