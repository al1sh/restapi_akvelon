import sys
sys.path.append("../")

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

    # *********** /tasks CRUD endpoints ***********

    def test_tasks_get(self):
        with app.app_context():
            response = self.app.get('/tasks')
            compare = [self.task2.to_dict(), self.task1.to_dict()]

            self.assertEqual(response.json, compare)
            self.assertEqual(response.status_code, 200)

    def test_tasks_post_correct(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'task3_test', 'status': 'done',
                             'project_id': 1, 'employee_id': 1}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(name='TEST_TASK').first()

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(new)

    def test_tasks_post_missing_project(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'task3_test', 'status': 'done',
                             'employee_id': 1}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(name='TEST_TASK').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(new)

    def test_tasks_post_without_name(self):
        with app.app_context():
            new_task_dict = {'description': 'task3_test', 'status': 'done',
                             'employee_id': 1}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(description='task3_test').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(new)

    def test_tasks_post_with_not_exisiting_project_id(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'task3_test', 'status': 'done',
                             'project_id': 99, 'employee_id': 1}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(name='TEST_TASK').first()

            self.assertEqual(response.status_code, 404)
            self.assertIsNone(new)

    def test_tasks_post_with_nonexisitent_employee_id(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'task3_test', 'status': 'done',
                             'project_id': 1, 'employee_id': 99}

            response = self.app.post('/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})

            new = Tasks.query.filter_by(name='TEST_TASK').first()

            self.assertEqual(response.status_code, 404)
            self.assertIsNone(new)

    def test_tasks_put_correct(self):
        with app.app_context():
            new_task_dict = {'id': '1', 'description': 'task1_put'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                    headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 204)
            self.assertEqual(t.description, 'task1_put')

    def test_tasks_put_without_id(self):
        with app.app_context():
            new_task_dict = {'description': 'task1_put'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                    headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(description='task1_put').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(t)

    def test_tasks_put_nonexistent_id(self):
        with app.app_context():
            new_task_dict = {'id': '99', 'description': 'task1_put'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                    headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=99).first()

            self.assertEqual(response.status_code, 404)
            self.assertIsNone(t)

    def test_tasks_put_nonexistent_project_id(self):
        with app.app_context():
            new_task_dict = {'id': '1', 'description': 'task1_put', 'project_id': '99'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                    headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 404)
            self.assertNotEqual(t.project_id, 99)

    def test_tasks_put_nonexistent_employee_id(self):
        with app.app_context():
            new_task_dict = {'id': '1', 'description': 'task1_put', 'employee_id': '99'}

            response = self.app.put('/tasks', data=json.dumps(new_task_dict),
                                    headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 404)
            self.assertNotEqual(t.employee_id, 99)

    def test_tasks_delete_correct(self):
        with app.app_context():
            new_task_dict = {'id': '1'}
            t = Tasks.query.filter_by(id=1).first()
            self.assertIsNotNone(t)

            response = self.app.delete('/tasks', data=json.dumps(new_task_dict),
                                       headers={"content-type": "application/json"})

            self.assertEqual(response.status_code, 204)
            t = Tasks.query.filter_by(id=1).first()
            self.assertIsNone(t)


    def test_delete_tasks_nonexistent_id(self):
        with app.app_context():
            new_task_dict = {'id': '99'}
            t = Tasks.query.filter_by(id=99).first()
            self.assertIsNone(t)

            response = self.app.delete('/tasks', data=json.dumps(new_task_dict),
                                       headers={"content-type": "application/json"})

            t = Tasks.query.filter_by(id=99).first()
            self.assertEqual(response.status_code, 404)
            self.assertIsNone(t)

    # ********* /employees CRUD endpoints *********

    def test_employees_get(self):
        with app.app_context():
            response = self.app.get('/employees')
            compare = [self.employee1.to_dict(), self.employee2.to_dict()]
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, compare)

    def test_employees_post_correct(self):
        with app.app_context():
            new_emp_dict = {'name': 'TEST_EMPLOYEE', 'gender': 'M'}

            emp3 = Tasks()
            emp3.from_dict(new_emp_dict)

            response = self.app.post('/employees', data=json.dumps(new_emp_dict),
                                     headers={"content-type": "application/json"})

            new = Employees.query.filter_by(name='TEST_EMPLOYEE').first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, new.to_dict())

    def test_employees_post_without_name(self):
        with app.app_context():
            new_emp_dict = {'gender': 'non-binary'}

            response = self.app.post('/employees', data=json.dumps(new_emp_dict),
                                     headers={"content-type": "application/json"})

            new_employee = Employees.query.filter_by(gender='non-binary').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(new_employee)

    def test_employees_put_correct(self):
        with app.app_context():
            new_dict = {'id': '1', 'name': 'test_put'}

            response = self.app.put('/employees', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Employees.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 204)
            self.assertEqual(t.name, 'test_put')

    def test_employees_put_nonexistent_id(self):
        with app.app_context():
            new_dict = {'id': '99', 'name': 'test_put'}

            response = self.app.put('/employees', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Employees.query.filter_by(name='test_put').first()

            self.assertEqual(response.status_code, 404)
            self.assertIsNone(t)

    def test_employees_put_without_id(self):
        with app.app_context():
            new_dict = {'name': 'test_put'}

            response = self.app.put('/employees', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Employees.query.filter_by(name='test_put').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(t)

    def test_employees_delete_correct(self):
        with app.app_context():
            new_dict = {'id': '1'}
            t = Employees.query.filter_by(id=1).first()
            self.assertIsNotNone(t)

            response = self.app.delete('/employees', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 204)

            t = Employees.query.filter_by(id=1).first()
            self.assertIsNone(t)

    def test_employees_delete_nonexistent_id(self):
        with app.app_context():
            new_dict = {'id': '99'}
            t = Employees.query.filter_by(id=99).first()
            self.assertIsNone(t)

            response = self.app.delete('/employees', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})

            self.assertEqual(response.status_code, 404)

    # ********* /projects CRUD endpoints *********

    def test_projects_get(self):
        with app.app_context():
            response = self.app.get('/projects')
            compare = [self.project2.to_dict(), self.project1.to_dict()]
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, compare)

    def test_projects_post_correct(self):
        with app.app_context():
            new_dict = {'name': 'TEST_PROJECT', 'code': 'RED'}

            emp3 = Employees()
            emp3.from_dict(new_dict)

            response = self.app.post('/projects', data=json.dumps(new_dict),
                                     headers={"content-type": "application/json"})

            new = Projects.query.filter_by(name='TEST_PROJECT').first()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, new.to_dict())

    def test_projects_post_without_name(self):
        with app.app_context():
            new_dict = {'code': 'TEST_CODE'}

            response = self.app.post('/projects', data=json.dumps(new_dict),
                                     headers={"content-type": "application/json"})

            new_project = Projects.query.filter_by(code='TEST_CODE').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(new_project)

    def test_projects_put_correct(self):
        with app.app_context():
            new_dict = {'id': '1', 'name': 'test_put'}

            response = self.app.put('/projects', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Projects.query.filter_by(id=1).first()

            self.assertEqual(response.status_code, 204)
            self.assertEqual(t.name, 'test_put')

    def test_projects_put_nonexistent_id(self):
        with app.app_context():
            new_dict = {'id': '99', 'name': 'test_put'}

            response = self.app.put('/projects', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Projects.query.filter_by(name='test_put').first()

            self.assertEqual(response.status_code, 404)
            self.assertIsNone(t)

    def test_projects_put_without_id(self):
        with app.app_context():
            new_dict = {'name': 'test_put'}

            response = self.app.put('/projects', data=json.dumps(new_dict),
                                    headers={"content-type": "application/json"})

            t = Projects.query.filter_by(name='test_put').first()

            self.assertEqual(response.status_code, 400)
            self.assertIsNone(t)

    def test_projects_delete_correct(self):
        with app.app_context():
            new_dict = {'id': '1'}
            t = Projects.query.filter_by(id=1).first()
            self.assertIsNotNone(t)

            response = self.app.delete('/projects', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 204)

            t = Projects.query.filter_by(id=1).first()
            self.assertIsNone(t)

    def test_projects_delete_nonexistent_id(self):
        with app.app_context():
            new_dict = {'id': '99'}
            t = Projects.query.filter_by(id=99).first()
            self.assertIsNone(t)

            response = self.app.delete('/projects', data=json.dumps(new_dict),
                                       headers={"content-type": "application/json"})

            self.assertEqual(response.status_code, 404)

    # *** Individual /projects/* endpoints ***

    def test_get_tasks_of_project_by_id_correct(self):
        with app.app_context():
            t = Projects.query.filter_by(id=1).first()
            tasks = []
            for task in t.tasks:
                tasks.append(task)

            response = self.app.get('/projects/1/tasks')

            self.assertEqual(response.json["tasks"], [test.to_dict() for test in tasks])
            self.assertEqual(response.status_code, 200)

    def test_get_tasks_of_project_by_id_nonexistent(self):
        with app.app_context():
            t = Projects.query.filter_by(id=99).first()
            self.assertIsNone(t)
            response = self.app.get('/projects/99/tasks')

            self.assertEqual(response.status_code, 404)

    def test_get_open_tasks_by_project_id_correct(self):
        with app.app_context():
            response = self.app.get('/projects/1/tasks/open')
            t = Projects.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                if task.status == "open":
                    tasks.append(task)

            self.assertEqual(response.json["open"], [test.to_dict() for test in tasks])
            self.assertEqual(response.status_code, 200)

    def test_get_open_tasks_by_project_id_with_nonexistent_id(self):
        with app.app_context():
            response = self.app.get('/projects/99/tasks/open')
            t = Projects.query.filter_by(id=99).first()
            self.assertIsNone(t)
            self.assertEqual(response.status_code, 404)

    def test_get_closed_tasks_by_project_id_correct(self):
        with app.app_context():
            response = self.app.get('/projects/1/tasks/done')
            t = Projects.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                if task.status == "done":
                    tasks.append(task)

            self.assertEqual(response.json["done"], [test.to_dict() for test in tasks])
            self.assertEqual(response.status_code, 200)

    def test_get_closed_tasks_by_project_id_with_nonexistent_id(self):
        with app.app_context():
            response = self.app.get('/projects/99/tasks/done')
            t = Projects.query.filter_by(id=99).first()
            self.assertIsNone(t)
            self.assertEqual(response.status_code, 404)

    # *** Individual /employee/* endpoints ***

    def test_get_employee_tasks_by_id_correct(self):
        with app.app_context():
            response = self.app.get('/employees/1/tasks')
            t = Employees.query.filter_by(id=1).first()

            tasks = []
            for task in t.tasks:
                tasks.append(task)

            self.assertEqual(response.json["tasks"], [test.to_dict() for test in tasks])
            self.assertEqual(response.status_code, 200)

    def test_get_employee_tasks_by_nonexistent_id(self):
        with app.app_context():
            response = self.app.get('/employees/99/tasks')
            t = Employees.query.filter_by(id=99).first()

            self.assertIsNone(t)
            self.assertEqual(response.status_code, 404)

    def test_post_existing_task_to_employee_by_id_correct(self):
        with app.app_context():

            new_task_dict = {'id': 1}

            response = self.app.post('/employees/1/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 204)

            e = Employees.query.filter_by(id=1).first()
            t = Tasks.query.filter_by(id=1).first()
            self.assertTrue(t in e.tasks)

    def test_post_new_task_to_employee_by_id_correct(self):
        with app.app_context():
            new_task_dict = {'name': 'TEST_TASK', 'description': 'TEST_DESCRIPTION', 'project_id': 1}

            response = self.app.post('/employees/1/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 201)

            e = Employees.query.filter_by(id=1).first()
            t = Tasks.query.filter_by(name='TEST_TASK').first()
            self.assertTrue(t in e.tasks)
            self.assertEqual(response.json, t.to_dict())

    def test_post_task_to_employee_by_id_with_nonexistent_id(self):
        with app.app_context():
            t = Tasks.query.filter_by(id=99).first()
            self.assertIsNone(t)

            new_task_dict = {'id': 99, 'name': 'TEST', 'project_id': 1}
            response = self.app.post('/employees/99/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 404)

            t = Tasks.query.filter_by(id=99).first()
            self.assertIsNone(t)

    def test_post_task_to_employee_by_id_without_name(self):
        with app.app_context():

            new_task_dict = {'description': 'TEST', 'project_id': 1}

            response = self.app.post('/employees/1/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 400)

            t = Tasks.query.filter_by(description='TEST').first()
            self.assertIsNone(t)

    def test_post_task_to_employee_by_id_without_project_id(self):
        with app.app_context():

            new_task_dict = {'name': 'TEST_TASK', 'description': 'TEST'}

            response = self.app.post('/employees/1/tasks', data=json.dumps(new_task_dict),
                                     headers={"content-type": "application/json"})
            self.assertEqual(response.status_code, 400)

            t = Tasks.query.filter_by(name='TEST_TASK').first()
            self.assertIsNone(t)

    def test_get_employee_tasks_by_id_from_project_id_correct(self):
        with app.app_context():
            response = self.app.get('/employees/2/2/tasks')
            t = Employees.query.filter_by(id=2).first()
            p = Projects.query.filter_by(id=2).first()

            task_list = t.tasks
            self.assertTrue(self.task2 in task_list)
            self.assertEqual(response.status_code, 200)

    def test_get_employee_tasks_by_id_from_project_id_nonexistent_project(self):
        with app.app_context():
            p = Projects.query.filter_by(id=99).first()
            self.assertIsNone(p)

            response = self.app.get('/employees/2/99/tasks')

            self.assertEqual(response.status_code, 404)

    def test_get_employee_tasks_by_id_from_project_id_nonexistent_employee(self):
        with app.app_context():
            e = Employees.query.filter_by(id=99).first()
            self.assertIsNone(e)

            response = self.app.get('/employees/99/2/tasks')

            self.assertEqual(response.status_code, 404)

    def test_get_open_tasks_by_employee_id_correct(self):
        with app.app_context():
            response = self.app.get('/employees/2/tasks/open')
            t = Employees.query.filter_by(id=2).first()
            tasks_open = list(filter((lambda x: x.status == "open"), t.tasks))

            self.assertEqual(response.json, {'tasks': [t.to_dict() for t in tasks_open]})
            self.assertEqual(response.status_code, 200)

    def test_get_open_tasks_by_employee_id_with_nonexistent_id(self):
        with app.app_context():
            e = Employees.query.filter_by(id=99).first()
            self.assertIsNone(e)

            response = self.app.get('/employees/99/tasks/open')

            self.assertEqual(response.status_code, 404)

    def test_get_done_tasks_by_employee_id_correct(self):
        with app.app_context():
            response = self.app.get('/employees/2/tasks/done')
            t = Employees.query.filter_by(id=2).first()
            tasks_open = list(filter((lambda x: x.status == "done"), t.tasks))

            self.assertEqual(response.json, {'tasks': [t.to_dict() for t in tasks_open]})
            self.assertEqual(response.status_code, 200)

    def test_get_done_tasks_by_employee_id_with_nonexistent_id(self):
        with app.app_context():
            e = Employees.query.filter_by(id=99).first()
            self.assertIsNone(e)

            response = self.app.get('/employees/99/tasks/done')

            self.assertEqual(response.status_code, 404)

    def test_patch_task_status_by_id_correct(self):
        with app.app_context():
            response = self.app.patch('/tasks/1')
            t = Tasks.query.filter_by(id=1).first()
            self.assertEqual(t.status, "done")

    #   *** Individual /tasks/* endpoints ***

    def test_patch_task_status_by_id_nonexistent_id(self):
        with app.app_context():
            t = Tasks.query.filter_by(id=99).first()
            self.assertIsNone(t)

            response = self.app.patch('/tasks/99')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()




