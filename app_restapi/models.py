from enum import Enum
from app_restapi import db
from datetime import datetime


class Status(Enum):
    open = 1
    done = 2


class Gender(Enum):
    F = 1
    M = 2


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    status = db.Column(db.Enum(Status))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project':
                {
                    'project_id': self.project_id,
                    'project_name': self.project.name
                }

        }

        if self.status:
            data['status'] = self.status.name

        if self.employee:
            data['employee'] = {'employee_id': self.employee_id,
                                'employee_name':  self.employee.name}
        return data

    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])

        if 'status' in data:
            db_field = Status[data['status']]
            setattr(self, 'status', db_field)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    code = db.Column(db.String(64))
    tasks = db.relationship("Task", backref="project", cascade="all, delete-orphan", lazy="dynamic")

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

    def from_dict(self, data):
        for field in ['name', 'code']:
            if field in data:
                setattr(self, field, data[field])


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.Enum(Gender))
    date_of_birth = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    tasks = db.relationship("Task", backref="employee", lazy="dynamic")

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'gender': Gender(self.gender).name,
            'tasks': [t.to_dict() for t in self.tasks]
        }

        if self.date_of_birth:
            data['date_of_birth'] = self.date_of_birth.strftime("%d-%m-%Y")

        if self.start_date:
            data['start_date'] = self.start_date.strftime("%d-%m-%Y")

        return data

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

        for field in ['date_of_birth', 'start_date']:
            if field in data:
                db_field = datetime.strptime(data[field], "%d-%m-%Y")
                setattr(self, field, db_field)

        if "gender" in data:
            db_field = Gender[data['gender']]
            setattr(self, "gender", db_field)

    def __repr__(self):
        return '<Employee {}>'.format(self.name)
