from app_restapi import app, db
from flask import jsonify,request
from app_restapi.models import Tasks, Employees, Projects
from app_restapi.errors import bad_request

# from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
# api = Api(app)
# ma = Marshmallow(app)


# # *** MARSHMALLOW SCHEMA
#
# class TaskSchema(ma.ModelSchema):
#     class Meta:
#         model = Tasks
#         fields = ('id', 'name', 'description', 'status', 'project')
#     # project = ma.Nested(ProjectSchema)
#
#
# class ProjectSchema(ma.ModelSchema):
#     class Meta:
#         model = Projects
#         fields = ('id', 'name', 'code', 'tasks')
#     # tasks = ma.Nested(TaskSchema(many=True))
#
# # *** ENDPOINTS ***
#
#
# class TaskCRUD(Resource):
#     def get(self):
#         tasks = Tasks.query.all()
#         task_schema = TaskSchema(many=True)
#         output = task_schema.dump(tasks).data
#         return jsonify({"tasks": output})
#
#
# api.add_resource(TaskCRUD, '/tasks')
#
#
# class ProjectCRUD(Resource):
#     def get(self):
#         projects = Projects.query.all()
#         project_schema = ProjectSchema(many=True)
#         output = project_schema.dump(projects).data
#         return jsonify({"projects": output})
#
#
# api.add_resource(ProjectCRUD, '/projects')


#       *** Tasks ***

@app.route('/tasks', methods=["GET", "POST", "PUT", "DELETE"])
def get_tasks():
    if request.method == "POST":
        pass

    if request.method == "GET":
        tasks = Tasks.query.all()
        return jsonify([task.to_dict() for task in tasks])


#       *** Employees ***

@app.route('/employees', methods=["GET", "POST", "PUT", "DELETE"])
def get_employees():
    if request.method == "GET":
        employees = Employees.query.all()
        return jsonify([emp.to_dict() for emp in employees])

    elif request.method == 'POST':
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


#       *** Projects ***

@app.route('/projects', methods=["GET", "POST", "PUT", "DELETE"])
def get_projects():
    if request.method == "GET":
        projects = Projects.query.all()
        return jsonify([proj.to_dict() for proj in projects])