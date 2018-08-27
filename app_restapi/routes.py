from app_restapi import app, db
from flask import jsonify,request
from app_restapi.models import Tasks, Employees, Projects
from app_restapi.errors import bad_request

#       *** Tasks ***


@app.route('/tasks', methods=["GET", "POST", "PUT", "DELETE"])
def get_tasks():
    if request.method == "GET":
        tasks = Tasks.query.all()
        return jsonify([task.to_dict() for task in tasks])

    if request.method == "POST":
        data = request.get_json() or {}
        if 'name' not in data or "project" not in data:
            return bad_request('must include name and project field')

        existing_project = Projects.query.filter_by(name=data['project']).first()

        if not existing_project:
            return bad_request("Project does not exist")

        t = Tasks()
        if 'employee' in data:
            existing_employee = Employees.query.filter_by(name=data['employee']).first()

            if not existing_employee:
                return bad_request("Employee does not exist")

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
        if 'name' not in data:
            return bad_request('must include task name')

        existing_task = Tasks.query.filter_by(name=data['name']).first()
        if not existing_task:
            return bad_request("task doesn't exist")

        response = jsonify(existing_task.to_dict())
        db.session.delete(existing_task)
        db.session.commit()

        response.status_code = 201
        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        t = Tasks.query.filter_by(id=data['id']).first()
        if not t:
            return bad_request("no such ID")

        if 'project' in data:
            existing_project = Projects.query.filter_by(name=data['project']).first()

            if not existing_project:
                return bad_request("Project does not exist")
            else:
                t.project = existing_project

        if 'employee' in data:
            existing_employee = Employees.query.filter_by(name=data['employee']).first()

            if not existing_employee:
                return bad_request("Employee does not exist")
            else:
                t.employee = existing_employee

        t.from_dict(data)

        db.session.commit()
        response = jsonify(t.to_dict())
        response.status_code = 201

        return response

#       *** Employees ***

@app.route('/employees', methods=["GET", "POST", "PUT", "DELETE"])
def get_employees():
    if request.method == "GET":
        employees = Employees.query.all()
        return jsonify([emp.to_dict() for emp in employees])

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'name' not in data:
            return bad_request('must include name field')
        
        # if User.query.filter_by(username=data['username']).first():
        #     return bad_request('please use a different username')
        # if User.query.filter_by(email=data['email']).first():
        #     return bad_request('please use a different email address')

        emp = Employees()
        emp.from_dict(data)
        db.session.add(emp)
        db.session.commit()
        response = jsonify(emp.to_dict())
        response.status_code = 201

        return response

    if request.method == "DELETE":
        data = request.get_json() or {}
        if 'name' not in data:
            return bad_request('must include employee name')

        existing_employee = Employees.query.filter_by(name=data['name']).first()
        if not existing_employee:
            return bad_request("employee doesn't exist")

        response = jsonify(existing_employee.to_dict())
        db.session.delete(existing_employee)
        db.session.commit()

        response.status_code = 201
        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        selected_employee = Employees.query.filter_by(id=data['id']).first()
        if not selected_employee:
            return bad_request("no such ID")

        selected_employee.from_dict(data)

        db.session.commit()
        response = jsonify(selected_employee.to_dict())
        response.status_code = 201

        return response


#       *** Projects ***

@app.route('/projects', methods=["GET", "POST", "PUT", "DELETE"])
def get_projects():
    if request.method == "GET":
        projects = Projects.query.all()
        return jsonify([proj.to_dict() for proj in projects])

    if request.method == 'POST':
        data = request.get_json(force=True) or {}

        if 'name' not in data:
            return bad_request('must include name field')

        # if User.query.filter_by(username=data['username']).first():
        #     return bad_request('please use a different username')
        # if User.query.filter_by(email=data['email']).first():
        #     return bad_request('please use a different email address')

        proj = Projects()
        proj.from_dict(data)
        db.session.add(proj)
        db.session.commit()
        response = jsonify(proj.to_dict())
        response.status_code = 201

        return response

    if request.method == "DELETE":
        data = request.get_json() or {}
        if 'name' not in data:
            return bad_request('must include project name')

        existing_project = Projects.query.filter_by(name=data['name']).first()
        if not existing_project:
            return bad_request("project doesn't exist")

        response = jsonify(existing_project.to_dict())
        db.session.delete(existing_project)
        db.session.commit()

        response.status_code = 201
        return response

    if request.method == "PUT":
        data = request.get_json() or {}
        if 'id' not in data:
            return bad_request('must include id field')

        selected_project = Projects.query.filter_by(id=data['id']).first()
        if not selected_project:
            return bad_request("no such ID")

        selected_project.from_dict(data)

        db.session.commit()
        response = jsonify(selected_project.to_dict())
        response.status_code = 201

        return response


@app.route("/projects/<int:id>/tasks", methods=["GET"])
def get_project_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return bad_request("project with given id does not exist")

    task_list = selected_project.tasks

    return jsonify({"tasks": [t.to_dict() for t in task_list]})


@app.route("/projects/<int:id>/tasks/open", methods=["GET"])
def get_project_open_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return bad_request("project with given id does not exist")

    task_list = selected_project.tasks
    open_tasks = list(filter((lambda x: x.status == "open"), task_list))
    return jsonify({"open": [t.to_dict() for t in open_tasks]})


@app.route("/projects/<int:id>/tasks/done", methods=["GET"])
def get_project_done_tasks(id):
    selected_project = Projects.query.filter_by(id=id).first()

    if not selected_project:
        return bad_request("project with given id does not exist")

    task_list = selected_project.tasks
    open_tasks = list(filter((lambda x: x.status == "done"), task_list))
    return jsonify({"open": [t.to_dict() for t in open_tasks]})


@app.route("/employees/<int:id>/tasks", methods=["GET", "POST"])
def employee_tasks_by_id(id):
    if request.method == "GET":
        selected_employee = Employees.query.filter_by(id=id).first()

        if not selected_employee:
            return bad_request("project with given id does not exist")

        task_list = selected_employee.tasks
        return jsonify({"tasks": [t.to_dict() for t in task_list]})

    elif request.method == "POST":
        selected_employee = Employees.query.filter_by(id=id).first()

        if not selected_employee:
            return bad_request("project with given id does not exist")

        data = request.get_json() or {}

        if 'id' in data:
            selected_task = Tasks.query.filter_by(id=data['id']).first()
            if not selected_task:
                return bad_request("no task with such ID")
            selected_task.employee = selected_employee

            db.session.commit()
            response = jsonify(selected_task.to_dict())
            response.status_code = 201

            return response

        else:
            if 'name' not in data or "project" not in data:
                return bad_request('must include name and project field')

            existing_project = Projects.query.filter_by(name=data['project']).first()
            if not existing_project:
                return bad_request("Project does not exist")

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
        return bad_request("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_from_project_id = list(filter((lambda x: x.project_id == int(proj_id)), task_list))

    return jsonify({"tasks": [t.to_dict() for t in tasks_from_project_id]})


@app.route("/employees/<int:emp_id>/tasks/open", methods=["GET"])
def get_emp_open_tasks(emp_id):
    selected_employee = Employees.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return bad_request("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "open"), task_list))

    return jsonify({"tasks": [t.to_dict() for t in tasks_open]})


@app.route("/employees/<int:emp_id>/tasks/done", methods=["GET"])
def get_emp_done_tasks(emp_id):
    selected_employee = Employees.query.filter_by(id=emp_id).first()

    if not selected_employee:
        return bad_request("project with given id does not exist")

    task_list = selected_employee.tasks
    tasks_open = list(filter((lambda x: x.status == "done"), task_list))

    return jsonify({"tasks": [t.to_dict() for t in tasks_open]})


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def patch_task_done(task_id):
    selected_task = Tasks.query.filter_by(id=task_id).first()
    if not selected_task:
        return bad_request("no such task ID")

    selected_task.status = 'done'

    db.session.commit()
    response = jsonify(selected_task.to_dict())
    response.status_code = 201

    return response


