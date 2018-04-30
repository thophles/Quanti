import os, re, dns.resolver, socket, smtplib
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from app.db import *
from app.forms import *
from app import *
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, configure_uploads, IMAGES
import flask_whooshalchemyplus as wa
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, \
     check_password_hash


#always configure app first
app = Flask(__name__)
Bootstrap(app)

photos = UploadSet('photos', IMAGES)

UPLOAD_FOLDER = '/capstoneApp/capstoneApp/projectPhotos'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://theowilliams:Franklin97@localhost:5432/capstone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_PHOTOS_DEST'] = '/app/static/img'
configure_uploads(app, photos)
app.config['SECRET_KEY'] = 'thisIsASecretKey'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
# engine = create_engine("postgresql://theowilliams:Franklin97@localhost:5432/capstone_db")
# # gives each user on the site a personalized session
# session_factory = sessionmaker(bind=engine)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login.init_app(app)
login.login_view = 'login'

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('home'))
        else:
            return render_template('logInError.html', message='Your account information cannot be found.')

    return render_template("index.html", form=form)

@app.route("/delete", methods=["POST", "GET"])
def delete(id):
    cartItem = ClassCart.query.filter_by(class_id=id).first()
    db.session.delete(cartItem)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/signup", methods=["POST", "GET"])
def signup():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, departmentone=form.departmentOne.data, departmenttwo=form.departmentTwo.data, grade=form.Grade.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("signup.html", form=form)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def home():

    # ("SELECT * FROM students WHERE email = :id", {"id": email})
    # classes = ClassCart.query.filter_by(student_id = current_user.id).all()
    classes = ClassCart.query.join(Classes, ClassCart.class_id==Classes.id).join(User, ClassCart.student_id == User.id).filter_by(id = current_user.id).all()
    print(classes)
    picks = Classes.query.filter(Classes.teacher_one >= 1).all()
    return render_template("mainfeedTest.html", classes=classes, picks=picks)

@app.route('/search')
def search():
    encoded = open(request.args.get('query'), encoding='utf-8')
    qResults = Classes.query.whoosh_search(encoded).all()
    if qResults is None:
        return render_template("search.html", message='No Classes Found.')

    return render_template("search.html", qResults=qResults)

@app.route('/courses', methods=["GET", "POST"])
@login_required
def course():
    courses = Classes.query.filter(Classes.teacher_one >= 1).all()

    return render_template("courses.html", courses=courses)


#image upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'photo' in request.files:
        # check if the post request has the file part
        filename = photos.save(request.files['photo'])
        return filename
    return redirect(url_for('home'))


@app.route('/user/<name>', methods=['POST'])
@login_required
def user(name):
    user = User.query.filter_by(id=current_user.id).first_or_404()

    return render_template('user.html', user=user)


@app.route('/description', methods=["POST", "GET"])
@app.route('/description/<int:id>', methods=["POST", "GET"])
def description(id):
    results = Classes.query.filter_by(id=id).first_or_404()
    followers = ClassCart.query.filter_by(class_id=id).all()
    comment = request.form.get("comment")
    if comment:
        newComment = Comments(comment_name=comment, comment_class=id)
        db.session.add(newComment)
        db.session.commit()

    commentQuery = Comments.query.filter(Comments.comment_class == id).all()
    return render_template("descriptionTest.html", results=results, description="hi", commentQuery=commentQuery, followers=followers)

@app.route('/add/<int:course>', methods=["POST"])
@login_required
def add(course):
    user = current_user.id
    newClass = ClassCart(student_id=user, class_id=course)
    db.session.add(newClass)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
     app.run(debug=True)
