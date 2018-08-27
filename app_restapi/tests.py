from flask import jsonify
from app_restapi import app, db
from app_restapi.models import Tasks, Employees, Projects
# from app_restapi.routes import *
import unittest
import json


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
        db.create_all()
        self.app = app.test_client()

        self.employee1 = Employees(name="John", gender='M', date_of_birth="01/05/1990", start_date="2001")
        self.employee2 = Employees(name="Mike", gender='M', date_of_birth="09/05/1999", start_date="2011")

        self.project1 = Projects(name="test1", code="red")
        self.project2 = Projects(name='test2', code="blue")

        self.task1 = Tasks(name='task1', description='task1_test', status='open',
                           project=self.project1)

        self.task2 = Tasks(name='task2', description='task2_test', status='done',
                           project=self.project2, employee=self.employee2)

        db.session.add_all([self.employee1, self.employee2])
        db.session.add_all([self.project1, self.project2])
        db.session.add_all([self.task1, self.task2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_tasks_get(self):
        with app.app_context():
            response = self.app.get('/tasks')
            compare = [self.task2.to_dict(), self.task1.to_dict()]
            self.assertEqual(response.json, compare)

    def test_employee_post(self):
        with app.app_context():
            new_task_dict = {'name': 'task3', 'description': 'task3_test', 'status': 'done',
                             'project_id': 1, 'employee_id': 1}

            task3 = Tasks()
            task3.from_dict(new_task_dict)

            task3.employee = self.employee1
            task3.project = self.project1

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            self.assertEqual(response.status_code, 201)



    def test_put_tasks(self):
        with app.app_context():
            new_task_dict = {'id': '1', 'description': 'task1_put'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            self.assertEqual(response.json, self.task1.to_dict())


if __name__ == '__main__':
    unittest.main()




