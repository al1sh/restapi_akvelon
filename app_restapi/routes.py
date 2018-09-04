from app_restapi import app, db
from flask import jsonify, request
from datetime import datetime
from app_restapi.models import Task, Employee, Project, Gender, Status
from app_restapi.errors import *


#   ****** /tasks/* CRUD routes ******

@app.route('/tasks', methods=["GET", "POST"])
def get_post_all_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        response = jsonify([task.to_dict() for task in tasks])
        response.status_code = 200
        return response

    if request.method == "POST":
        data = request.get_json() or {}
        if 'name' not in data or "project_id" not in data:
            return bad_request('must include name and project_id field')

        existing_project = Project.query.filter_by(id=data['project_id']).first()

        if not existing_project:
            return not_found("Project with such ID not exist")

        t = Task(project=existing_project)

        if 'employee_id' in data:
            existing_employee = Employee.query.filter_by(id=data['employee_id']).first()

            if not existing_employee:
                return not_found("Employee with such ID does not exist")

            t.employee = existing_employee

        if 'status' in data:
            try:
                status = Status[data["status"]]
            except Exception as e:
                return bad_request("incorrect status [open, done]")

        t.from_dict(data)
        db.session.add(t)
        db.session.commit()

        response = jsonify(t.to_dict())
        response.status_code = 201

        return response


@app.route("/tasks/<int:task_id>", methods=["GET", "PUT", "DELETE"])
def get_put_delete_by_task_id(task_id):
    if request.method == 'GET':
        existing_task = Task.query.filter_by(id=task_id).first()

        if not existing_task:
            return not_found("task with such ID does not exist")

        response = jsonify(existing_task.to_dict())
        response.status_code = 200
        return response

    if request.method == "DELETE":
        existing_task = Task.query.filter_by(id=task_id).first()
        if not existing_task:
            return not_found("task ID doesn't exist")

        response = jsonify()
        response.status_code = 204

        db.session.delete(existing_task)
        db.session.commit()

        return response

    if request.method == "PUT":
        data = request.get_json() or {}

        t = Task.query.filter_by(id=task_id).first()
        if not t:
            return not_found("no such task with such ID")

        # reassign if project id provided
        if 'project_id' in data:
            existing_project = Project.query.filter_by(id=data['project_id']).first()

            if not existing_project:
                return not_found("Project with such ID does not exist")
            else:
                t.project = existing_project

        if 'employee_id' in data:
            existing_employee = Employee.query.filter_by(id=data['employee_id']).first()

            if not existing_employee:
                return not_found("Employee with such ID does not exist")
            else:
                t.employee = existing_employee

        if 'status' in data:
            try:
                status = Status[data["status"]]
            except Exception as e:
                return bad_request("incorrect status [open/done]")

        t.from_dict(data)
        db.session.commit()

        response = jsonify()
        response.status_code = 204

        return response


#   ******* /employees/* routes *******


@app.route('/employees', methods=["GET", "POST"])
def get_employees():
    if request.method == "GET":
        employees = Employee.query.all()

        response = jsonify([emp.to_dict() for emp in employees])
        response.status_code = 200
        return response

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'name' not in data:
            return bad_request('must include name field')

        if 'start_date' in data:
            try:
                start_date = datetime.strptime(data['start_date'], "%d-%m-%Y")

            except Exception as e:
                return bad_request("incorrect start_date format")

        if 'date_of_birth' in data:
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], "%d-%m-%Y")

            except Exception as e:
                return bad_request("incorrect date_of_birth format")

        if "gender" in data:
            try:
                gender = Gender[data['gender']]
            except Exception as e:
                return bad_request('incorrect gender [M/F]')

        emp = Employee()
        emp.from_dict(data)

        db.session.add(emp)
        db.session.commit()

        response = jsonify(emp.to_dict())
        response.status_code = 201

        return response


@app.route("/employees/<int:employee_id>", methods=["GET", "PUT", "DELETE"])
def get_put_delete_by_employee_id(employee_id):
    if request.method == 'GET':
        existing_employee = Employee.query.filter_by(id=employee_id).first()

        if not existing_employee:
            return not_found("employee with such ID does not exist")

        response = jsonify(existing_employee.to_dict())
        response.status_code = 200
        return response

    if request.method == "DELETE":
        existing_employee = Employee.query.filter_by(id=employee_id).first()
        if not existing_employee:
            return not_found("employee with such ID doesn't exist")

        db.session.delete(existing_employee)
        db.session.commit()

        response = jsonify()
        response.status_code = 204
        return response

    if request.method == "PUT":
        data = request.get_json() or {}

        selected_employee = Employee.query.filter_by(id=employee_id).first()
        if not selected_employee:
            return not_found("no employee with such ID")

        if 'start_date' in data:
            try:
                start_date = datetime.strptime(data['start_date'], "%d-%m-%Y")

            except Exception as e:
                return bad_request("incorrect start_date format")

        if 'date_of_birth' in data:
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], "%d-%m-%Y")

            except Exception as e:
                return bad_request("incorrect date_of_birth format")

        if "gender" in data:
            try:
                gender = Gender[data['gender']]
            except Exception as e:
                return bad_request('incorrect gender [M/F]')

        selected_employee.from_dict(data)
        db.session.commit()

        response = jsonify()
        response.status_code = 204

        return response


#   ****** /projects/* routes ******

@app.route('/projects', methods=["GET", "POST"])
def get_projects():
    if request.method == "GET":
        projects = Project.query.all()
        response = jsonify([proj.to_dict() for proj in projects])
        response.status_code = 200
        return response

    elif request.method == 'POST':
        data = request.get_json(force=True) or {}

        if 'name' not in data:
            return bad_request('must include name field')

        proj = Project()
        proj.from_dict(data)

        db.session.add(proj)
        db.session.commit()

        response = jsonify(proj.to_dict())
        response.status_code = 201

        return response


@app.route("/projects/<int:project_id>", methods=["GET", "PUT", "DELETE"])
def get_put_delete_by_project_id(project_id):
    if request.method == 'GET':
        existing_project = Project.query.filter_by(id=project_id).first()

        if not existing_project:
            return not_found("project with such ID does not exist")

        response = jsonify(existing_project.to_dict())
        response.status_code = 200
        return response

    if request.method == "DELETE":

        existing_project = Project.query.filter_by(id=project_id).first()
        if not existing_project:
            return not_found("project with such ID does not exist")

        db.session.delete(existing_project)
        db.session.commit()

        response = jsonify()
        response.status_code = 204
        return response

    elif request.method == "PUT":
        data = request.get_json() or {}

        selected_project = Project.query.filter_by(id=project_id).first()
        if not selected_project:
            return not_found("no project with such ID")

        selected_project.from_dict(data)
        db.session.commit()

        response = jsonify(selected_project.to_dict())
        response.status_code = 204

        return response


#           ******* Individual endpoints *******

@app.route("/projects/<int:id>/tasks", methods=["GET"])
def get_project_tasks(id):
    selected_project = Project.query.filter_by(id=id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_project.tasks

    response = jsonify({"tasks": [t.to_dict() for t in task_list]})
    response.status_code = 200
    return response


@app.route("/projects/<int:id>/tasks/open", methods=["GET"])
def get_project_open_tasks(id):
    selected_project = Project.query.filter_by(id=id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_project.tasks
    open_tasks = list(filter((lambda x: x.status == "open"), task_list))

    response = jsonify({"open": [t.to_dict() for t in open_tasks]})
    response.status_code = 200
    return response


@app.route("/projects/<int:id>/tasks/done", methods=["GET"])
def get_project_done_tasks(id):
    selected_project = Project.query.filter_by(id=id).first()

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
        selected_employee = Employee.query.filter_by(id=id).first()

        if not selected_employee:
            return not_found("project with given id does not exist")

        task_list = selected_employee.tasks
        response = jsonify({"tasks": [t.to_dict() for t in task_list]})
        response.status_code = 200
        return response

    elif request.method == "POST":
        selected_employee = Employee.query.filter_by(id=id).first()

        if not selected_employee:
            return not_found("project with given id does not exist")

        data = request.get_json() or {}

        if 'name' not in data or "project_id" not in data:
            return bad_request('must include name and project_id field')

        existing_project = Project.query.filter_by(id=data['project_id']).first()
        if not existing_project:
            return not_found("Project with such ID does not exist")

        if 'status' in data:
            try:
                status = Status[data["status"]]
            except Exception as e:
                return bad_request("incorrect status [open, done]")

        t = Task(employee=selected_employee, project=existing_project)
        t.from_dict(data)

        db.session.add(t)
        db.session.commit()

        response = jsonify(t.to_dict())
        response.status_code = 201
        return response


@app.route("/employees/<int:emp_id>/<int:proj_id>/tasks", methods=["GET"])
def get_emp_proj_tasks(emp_id, proj_id):
    selected_employee = Employee.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("employee with given id does not exist")

    selected_project = Project.query.filter_by(id=proj_id).first()

    if not selected_project:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_from_project_id = list(filter((lambda x: x.project_id == int(proj_id)), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_from_project_id]})
    response.status_code = 200
    return response


@app.route("/employees/<int:emp_id>/tasks/open", methods=["GET"])
def get_emp_open_tasks(emp_id):
    selected_employee = Employee.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "open"), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_open]})
    response.status_code = 200
    return response


@app.route("/employees/<int:emp_id>/tasks/done", methods=["GET"])
def get_emp_done_tasks(emp_id):
    selected_employee = Employee.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return not_found("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "done"), task_list))

    response = jsonify({"tasks": [t.to_dict() for t in tasks_open]})
    response.status_code = 200
    return response


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def patch_task_done(task_id):
    selected_task = Task.query.filter_by(id=task_id).first()
    if not selected_task:
        return not_found("no such task ID")

    selected_task.status = Status.done
    db.session.commit()

    response = jsonify()
    response.status_code = 204

    return response
