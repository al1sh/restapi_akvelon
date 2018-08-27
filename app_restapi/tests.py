from app_restapi import app, db
from app_restapi.models import Tasks, Employees, Projects
from app_restapi.routes import *
import unittest
import json

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.employee1 = Employees(name="John", gender='M', date_of_birth="01/05/1990", start_date="2001")
        self.employee2 = Employees(name="Mike", gender='M', date_of_birth="09/05/1999", start_date="2011")
        self.test_employee = Employees()

        self.project1 = Projects(name="test1", code="red")
        self.project2 = Projects(name='test2', code="blue")
        self.test_project = Projects

        self.task1 = Tasks(name='task1', description='task1_test', status='open',
                           project=self.project1)
        self.task2 = Tasks(name='task2', description='task2_test', status='done',
                      project=self.project2, employee=self.employee2)
        self.test_task = Tasks()

        db.session.add_all([self.employee1, self.employee2])
        db.session.add_all([self.project1, self.project2])
        db.session.add_all([self.task1, self.task2])

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_employee_exist(self):
        response = self.app.get('/tasks')
        print(response.json)
        self.assertEqual(response.status, '200')


if __name__ == '__main__':
    unittest.main()




