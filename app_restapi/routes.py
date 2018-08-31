from app_restapi import app, db
from flask import jsonify, request
from app_restapi.models import Tasks, Employees, Projects
from app_restapi.errors import *


#   ****** /tasks/* routes ******


@app.route('/tasks', methods=["GET", "POST", "PUT", "DELETE"])
def get_tasks():
    if request.method == "GET":
        tasks = Tasks.query.all()
        response = jsonify([task.to_dict() for task in tasks])
        response.status_code = 200
        return response

    if request.method == "POST":
        data = request.get_json() or {}
        if 'name' not in data or "project_id" not in data:
            return bad_request('must include name and project_id field')

        existing_project = Projects.query.filter_by(id=data['project_id']).first()

        if not existing_project:
            return not_found("Project with such ID not exist")

        t = Tasks()
        if 'employee_id' in data:
            existing_employee = Employees.query.filter_by(id=data['employee_id']).first()

            if not existing_employee:
                return not_found("Employee with such ID does not exist")

            t = Tasks(employee=existing_employee, project=existing_project)

        else:
            t = Tasks(project=existing_project)

        t.from_dict(data)
        db.session.add(t)
        db.session.commit()

        response = jsonify(t.to_dict())
        response.status_code = 201

        return response

    if request.method == "DELETE":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include task ID')

        existing_task = Tasks.query.filter_by(id=data['id']).first()
        if not existing_task:
            return not_found("task ID doesn't exist")

        response = jsonify()
        response.status_code = 204

        db.session.delete(existing_task)
        db.session.commit()

        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        t = Tasks.query.filter_by(id=data['id']).first()
        if not t:
            return not_found("no such task with such ID")

        if 'project_id' in data:
            existing_project = Projects.query.filter_by(id=data['project_id']).first()

            if not existing_project:
                return not_found("Project with such ID does not exist")
            else:
                t.project = existing_project

        if 'employee_id' in data:
            existing_employee = Employees.query.filter_by(id=data['employee_id']).first()

            if not existing_employee:
                return not_found("Employee with such ID does not exist")
            else:
                t.employee = existing_employee

        t.from_dict(data)
        db.session.commit()

        response = jsonify()
        response.status_code = 204

        return response

#   ******* /employees/* routes *******


@app.route('/employees', methods=["GET", "POST", "PUT", "DELETE"])
def get_employees():
    if request.method == "GET":
        employees = Employees.query.all()

        response = jsonify([emp.to_dict() for emp in employees])
        response.status_code = 200
        return response

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'name' not in data:
            return bad_request('must include name field')

        emp = Employees()
        emp.from_dict(data)

        db.session.add(emp)
        db.session.commit()

        response = jsonify(emp.to_dict())
        response.status_code = 201

        return response

    if request.method == "DELETE":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include employee ID')

        existing_employee = Employees.query.filter_by(id=data['id']).first()
        if not existing_employee:
            return not_found("employee with such ID doesn't exist")

        db.session.delete(existing_employee)
        db.session.commit()

        response = jsonify()
        response.status_code = 204
        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        selected_employee = Employees.query.filter_by(id=data['id']).first()
        if not selected_employee:
            return not_found("no employee with such ID")

        selected_employee.from_dict(data)
        db.session.commit()

        response = jsonify()
        response.status_code = 204

        return response


#   ****** /projects/* routes ******

@app.route('/projects', methods=["GET", "POST", "PUT", "DELETE"])
def get_projects():
    if request.method == "GET":
        projects = Projects.query.all()
        response = jsonify([proj.to_dict() for proj in projects])
        response.status_code = 200
        return response

    if request.method == 'POST':
        data = request.get_json(force=True) or {}

        if 'name' not in data:
            return bad_request('must include name field')

        proj = Projects()
        proj.from_dict(data)

        db.session.add(proj)
        db.session.commit()

        response = jsonify(proj.to_dict())
        response.status_code = 201

        return response

    if request.method == "DELETE":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include project name')

        existing_project = Projects.query.filter_by(id=data['id']).first()
        if not existing_project:
            return not_found("project with such ID does not exist")

        db.session.delete(existing_project)
        db.session.commit()

        response = jsonify()
        response.status_code = 204
        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        selected_project = Projects.query.filter_by(id=data['id']).first()
        if not selected_project:
            return not_found("no project with such ID")

        selected_project.from_dict(data)
        db.session.commit()

        response = jsonify(selected_project.to_dict())
        response.status_code = 204

        return response


@app.route("/projects/<int:id>/tasks", methods=["GET"])
def get_project_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_project.tasks

    response = jsonify({"tasks": [t.to_dict() for t in task_list]})
    response.status_code = 200
    return response


@app.route("/projects/<int:id>/tasks/open", methods=["GET"])
def get_project_open_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_project.tasks
    open_tasks = list(filter((lambda x: x.status == "open"), task_list))

    response = jsonify({"open": [t.to_dict() for t in open_tasks]})
    response.status_code = 200
    return response


@app.route("/projects/<int:id>/tasks/done", methods=["GET"])
def get_project_done_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_project.tasks
    open_tasks = list(filter((lambda x: x.status == "done"), task_list))

    response = jsonify({"done": [t.to_dict() for t in open_tasks]})
    response.status_code = 200
    return response


@app.route("/employees/<int:id>/tasks", methods=["GET", "POST"])
def employee_tasks_by_id(id):
    if request.method == "GET":
        selected_employee = Employees.query.filter_by(id=id).first()

        if not selected_employee:
            return not_found("project with given id does not exist")

        task_list = selected_employee.tasks
        response = jsonify({"tasks": [t.to_dict() for t in task_list]})
        response.status_code = 200
        return response

    elif request.method == "POST":
        selected_employee = Employees.query.filter_by(id=id).first()

        if not selected_employee:
            return not_found("project with given id does not exist")

        data = request.get_json() or {}

        # reassign existing task
        if 'id' in data:
            selected_task = Tasks.query.filter_by(id=data['id']).first()
            if not selected_task:
                return not_found("no task with such ID")
            selected_task.employee = selected_employee

            db.session.commit()
            response = jsonify(selected_task.to_dict())
            response.status_code = 204

            return response

        # if id is not send the task will be created
        else:
            if 'name' not in data or "project_id" not in data:
                return bad_request('must include name and project_id field')

            existing_project = Projects.query.filter_by(id=data['project_id']).first()
            if not existing_project:
                return not_found("Project with such ID does not exist")

            t = Tasks(employee=selected_employee, project=existing_project)
            t.from_dict(data)

            db.session.add(t)
            db.session.commit()

            response = jsonify(t.to_dict())
            response.status_code = 201
            return response


@app.route("/employees/<int:emp_id>/<int:proj_id>/tasks", methods=["GET"])
def get_emp_proj_tasks(emp_id, proj_id):
    selected_employee = Employees.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("employee with given id does not exist")

    selected_project = Projects.query.filter_by(id=proj_id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_from_project_id = list(filter((lambda x: x.project_id == int(proj_id)), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_from_project_id]})
    response.status_code = 200
    return response


@app.route("/employees/<int:emp_id>/tasks/open", methods=["GET"])
def get_emp_open_tasks(emp_id):
    selected_employee = Employees.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "open"), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_open]})
    response.status_code = 200
    return response


@app.route("/employees/<int:emp_id>/tasks/done", methods=["GET"])
def get_emp_done_tasks(emp_id):
    selected_employee = Employees.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "done"), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_open]})
    response.status_code = 200
    return response


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def patch_task_done(task_id):
    selected_task = Tasks.query.filter_by(id=task_id).first()
    if not selected_task:
        return not_found("no such task ID")

    selected_task.status = 'done'
    db.session.commit()

    response = jsonify()
    response.status_code = 204

    return response
