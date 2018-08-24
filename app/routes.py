from app import app, db
from flask import jsonify,request
from flask_marshmallow import Marshmallow
from app.models import Task, Employee, Project
import json

ma = Marshmallow(app)

class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task

# *** Tasks ***
@app.route('/tasks', methods=["GET", "POST", "PUT", "DELETE"])
def get_tasks():
    if request.method == "POST":
        # result = ""
        # for key, value in request.form:
        #     result += key + value
        #
        # return result + "200"

        # post_json_raw = request.get_json(force=True)
        # got = json.loads(post_json_raw)

        return jsonify(request.get_json(force=True))
        # post_dict = json.load(post_json_raw)
        # name = post_dict["name"]

        # description = request.values.get("description")
        # status = request.values.get("status")
        #
        # if name and description and status:
        #     t = Task(name, description, status)
        #     db.session.add(t)
        #     db.session.commit()
        #     return "200"

        # else:
        print(post_json_raw)
        return "OK"

    if request.method == "GET":
        tasks = Task.query.all()
        task_schema = TaskSchema(many=True)
        output = task_schema.dump(tasks).data
        return jsonify({"tasks": output})





# *** Employees ***
@app.route('/index', methods=["POST"])
def index():
    if request.method == "POST":
        return "Hello, World!"