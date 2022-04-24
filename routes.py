from flask import redirect, render_template, session, request

from app import app
from entities import Worker
from functions import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        password = request.form["password"]
        retyped_password = request.form["re-typed password"]
        error_messages = get_worker_creation_error_messages(name, password, retyped_password)
        if error_messages:
            return render_template("register.html", messages=error_messages)
        create_worker(name, password)
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]
    worker = get_worker_by_name_and_password(name, password)
    if not worker:
        return render_template("index.html", message="Incorrect username or password!")
    session["name"] = worker.name
    session["is_supervisor"] = worker.is_supervisor
    return redirect("/workers/" + str(worker.id))

@app.route("/logout", methods=["POST"])
def logout():
    del session["name"]
    return redirect("/")

@app.route("/workers/", methods=["GET"])
def workers():
    workers = get_all_workers()
    return render_template("workers.html", workers=workers)

@app.route("/workers/<int:id>", methods=["GET"])
def worker(id):
    name = get_worker_name_by_id(id)
    if not name:
        return redirect("/")
    return render_template("profile.html", name=name, id=id)

@app.route("/projects/<int:id>", methods=["GET"])
def project(id):
    project = get_project_by_id(id)
    project_workers = get_workers_by_project_id(id)
    available_workers = get_all_free_workers()
    if not project:
        return redirect("/")
    return render_template("project.html", project=project, project_workers=project_workers,
                            available_workers=available_workers, is_supervisor = True)

@app.route("/projects/<int:project_id>/add_worker/<int:worker_id>", methods=["POST"])
def worker_to_project(project_id, worker_id):
    project = get_project_by_id(project_id)
    worker = get_worker_by_id(worker_id)
    if not project or not worker:
        return redirect("/projects/"+str(project_id))
    add_worker_to_project(project_id, worker_id)
    return redirect("/projects/"+str(project_id))

@app.route("/projects", methods=["GET"])
def manage_projects():
    all_projects = get_all_projects()
    return render_template("project_management.html", projects=all_projects, is_supervisor = True)

@app.route("/create_project", methods=["POST"])
def create_project():
    name = request.form["name"]
    save_project(name)
    return redirect("/projects")

@app.route("/workers/<int:id>/supervisor-request", methods=["POST"])
def supervisor_request(id):
    supervisors = get_supervisors_sorted_by_seniority()
    if not supervisors:
        grant_supervisor_status(id)
        session["is_supervisor"] = True
    else:
        print("request supervisor status from most senior supervisor")
    return redirect("/workers/" + str(id))

@app.route("/workers/<int:id>/worker-request", methods=["POST"])
def worker_request(id):
    supervisors = get_supervisors_sorted_by_seniority()
    if supervisors:
        remove_supervisor_status(id)
        session["is_supervisor"] = False
    else:
        print("Someone needs to be supervisor!")
    return redirect("/workers/" + str(id))