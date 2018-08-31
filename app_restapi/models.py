from app_restapi import db


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

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'project':
                {
                    'project_id': self.project_id,
                    'project_name': self.project.name
                }

        }
        if self.employee:
            data['employee'] = {'employee_id': self.employee_id,
                                'employee_name':  self.employee.name}
        return data

    def from_dict(self, data):
        for field in ['name', 'description', 'status']:
            if field in data:
                setattr(self, field, data[field])


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

    def from_dict(self, data):
        for field in ['name', 'code']:
            if field in data:
                setattr(self, field, data[field])


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
