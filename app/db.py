from flask import Flask, render_template, request, redirect, url_for
import sys
from app import login
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemyplus as wa
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, \
     check_password_hash

#always configure app first
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://theowilliams:Franklin97@localhost:5432/capstone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Classes(db.Model):
    __tablename__ = 'classes'
    __searchable__ = ['name', 'department', 'teacher_one']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    description = db.Column(db.String)
    semester = db.Column(db.String(100))
    teacher_one = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'),
        nullable=False)
    teacher_two = db.Column(db.Integer)
    teachers = db.relationship('Teacher',
        backref='classes', lazy=True)

wa.whoosh_index(app, Classes)

class Comments(db.Model):
    __tablename__ = 'comments'
    __searchable__ = ['comment_name','comment_class']
    id = db.Column(db.Integer, primary_key=True)
    comment_name = db.Column(db.String(200))
    comment_class = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    classes = db.relationship('Classes', backref='classes', lazy=True)


class ClassCart(db.Model):
    __tablename__ = 'class_cart'
    __searchable__ = ['student_id', 'class_id']
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    user = db.relationship('User', backref='students', lazy=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    classes = db.relationship('Classes', backref='cartclasses', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'students'
    __searchable__ = ['name', 'email', 'password']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    departmentone = db.Column(db.String, nullable=False)
    departmenttwo = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Teacher(db.Model):
        __tablename__ = 'teachers'
        __searchable__ = ['teacher_id', 'teacher_name']
        teacher_id = db.Column(db.Integer, primary_key=True)
        teacher_name = db.Column(db.String(80),nullable=False)

wa.whoosh_index(app, Teacher)
