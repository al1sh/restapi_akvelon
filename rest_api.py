from app_restapi import app, db
from app_restapi.models import Tasks, Employees, Projects


@app.shell_context_processor
def make_context_processor():
    return {"db": db, 'Tasks': Tasks, 'Employees': Employees, 'Projects': Projects}

