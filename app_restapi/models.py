from app_restapi import db


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
#
# class Posts(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    status = db.Column(db.String(64))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __repr__(self):
        return '<Task {}>'.format(self.name)

    def to_dict(self, with_project=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'project': self.project.name
        }
        if self.employee:
            data['employee'] = self.employee.name

        return data


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    code = db.Column(db.String(64))
    tasks = db.relationship("Tasks", backref="project", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return '<Project {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'tasks': [t.to_dict() for t in self.tasks]
        }

        return data


class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    date_of_birth = db.Column(db.String(64))
    start_date = db.Column(db.String(64))
    tasks = db.relationship("Tasks", backref="employee", lazy="dynamic")

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'start_date': self.start_date,
            'tasks': [t.to_dict() for t in self.tasks]
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'gender', 'date_of_birth', 'start_date']:
            if field in data:
                setattr(self, field, data[field])


    def __repr__(self):
        return '<Employee {}>'.format(self.name)