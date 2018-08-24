from app import db
from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256), index=True)
    status = db.Column(db.String(64), index=True)
    employee = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=True)
    project = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __repr__(self):
        return '<Task {}>'.format(self.name)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    code = db.Column(db.String(64), index=True, unique=True)
    tasks = db.relationship("Task", backref="from_project", lazy="dynamic")

    def __repr__(self):
        return '<Project {}>'.format(self.name)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    gender = db.Column(db.String(64))
    date_of_birth = db.Column(db.String(64))
    start_date = db.Column(db.String(64))

    def __repr__(self):
        return '<Employee {}>'.format(self.name)