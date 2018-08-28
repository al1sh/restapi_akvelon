from app_restapi import app, db
from app_restapi.models import Tasks, Employees, Projects
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

        self.task2 = Tasks(name='task2', description='task2_test', status='open',
                           project=self.project2, employee=self.employee2)

        db.session.add_all([self.employee1, self.employee2])
        db.session.add_all([self.project1, self.project2])
        db.session.add_all([self.task1, self.task2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ****** /tasks ***********
    def test_tasks_get(self):
        with app.app_context():
            response = self.app.get('/tasks')
            compare = [self.task2.to_dict(), self.task1.to_dict()]
            self.assertEqual(response.json, compare)

    def test_tasks_post(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'task3_test', 'status': 'done',
                             'project_id': 1, 'employee_id': 1}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(name='TEST_TASK').first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, new.to_dict())

    def test_put_tasks(self):
        with app.app_context():
            new_task_dict = {'id': '1', 'description': 'task1_put'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=1).first()
            self.assertEqual(t.description, 'task1_put')

    def test_delete_tasks(self):
        with app.app_context():
            new_task_dict = {'id': '1'}

            response = self.app.delete('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=1).first()
            self.assertFalse(t)

    # ******** /employees *********

    def test_emp_get(self):
        with app.app_context():
            response = self.app.get('/employees')
            compare = [self.employee2.to_dict(), self.employee1.to_dict()]
            self.assertEqual(response.status_code, 200)

    def test_emp_post(self):
        with app.app_context():
            new_emp_dict = {'name': 'TEST_EMP', 'gender': 'M'}

            emp3 = Tasks()
            emp3.from_dict(new_emp_dict)

            response = self.app.post('/employees', data=json.dumps(new_emp_dict),
                                     headers={"content-type": "application/json"})

            new = Employees.query.filter_by(name='TEST_EMP').first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, new.to_dict())

    def test_put_emp(self):
        with app.app_context():
            new_dict = {'id': '1', 'name': 'test_put'}

            response = self.app.put('/employees', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Employees.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(t.name, 'test_put')

    def test_delete_emp(self):
        with app.app_context():
            new_dict = {'id': '1'}

            response = self.app.delete('/employees', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})

            t = Employees.query.filter_by(id=1).first()
            self.assertFalse(t)

    # ******** /employees *********

    def test_proj_get(self):
        with app.app_context():
            response = self.app.get('/projects')
            # compare = [self.employee2.to_dict(), self.employee1.to_dict()]
            self.assertEqual(response.status_code, 200)

    def test_proj_post(self):
        with app.app_context():
            new_dict = {'name': 'TEST_PROJECT', 'code': 'RED'}

            emp3 = Employees()
            emp3.from_dict(new_dict)

            response = self.app.post('/projects', data=json.dumps(new_dict),
                                     headers={"content-type": "application/json"})

            new = Projects.query.filter_by(name='TEST_PROJECT').first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, new.to_dict())

    def test_proj_emp(self):
        with app.app_context():
            new_dict = {'id': '1', 'name': 'test_put'}

            response = self.app.put('/projects', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Projects.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(t.name, 'test_put')

    def test_delete_proj(self):
        with app.app_context():
            new_dict = {'id': '1'}

            response = self.app.delete('/projects', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})

            t = Projects.query.filter_by(id=1).first()
            self.assertFalse(t)

    # *** Individual Endpoints ***

    def test_proj_tasks(self):
        with app.app_context():
            response = self.app.get('/projects/1/tasks')
            t = Projects.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                tasks.append(task)

            self.assertEqual(response.json["tasks"], [test.to_dict() for test in tasks])

    def test_proj_tasks_open(self):
        with app.app_context():
            response = self.app.get('/projects/1/tasks/open')
            t = Projects.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                if task.status == "open":
                    tasks.append(task)

            self.assertEqual(response.json["open"], [test.to_dict() for test in tasks])

    def test_emp_by_id_get(self):
        with app.app_context():
            response = self.app.get('/employees/1/tasks')
            t = Employees.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                tasks.append(task)

            self.assertEqual(response.json["tasks"], [test.to_dict() for test in tasks])

    def test_emp_by_id_post(self):
        with app.app_context():

            new_task_dict = {'id': 1}

            response = self.app.post('/employees/1/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            e = Employees.query.filter_by(id=1).first()
            t = Tasks.query.filter_by(id=1).first()

            self.assertTrue(t in e.tasks)

    def test_emp_by_id_get(self):
        with app.app_context():
            response = self.app.get('/employees/2/2/tasks')
            t = Employees.query.filter_by(id=2).first()
            p = Projects.query.filter_by(id=2).first()

            task_list = t.tasks
            self.assertTrue(self.task2 in task_list)
            self.assertEqual(response.status_code, 200)

    def test_emp_by_id_open(self):
        with app.app_context():
            response = self.app.get('/employees/2/tasks/open')
            t = Employees.query.filter_by(id=2).first()
            tasks_open = list(filter((lambda x: x.status == "open"), t.tasks))

            self.assertEqual(response.json, {'tasks': [t.to_dict() for t in tasks_open]})

    def test_emp_by_id_done(self):
        with app.app_context():
            response = self.app.get('/employees/2/tasks/done')
            t = Employees.query.filter_by(id=2).first()
            tasks_open = list(filter((lambda x: x.status == "done"), t.tasks))

            self.assertEqual(response.json, {'tasks': [t.to_dict() for t in tasks_open]})

    def test_emp_by_id_done(self):
        with app.app_context():
            response = self.app.patch('/tasks/1')
            t = Tasks.query.filter_by(id=1).first()
            self.assertEqual(t.status, "done")


if __name__ == '__main__':
    unittest.main()




