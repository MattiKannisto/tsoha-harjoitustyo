from flask import redirect, render_template, session, request, abort

from app import app
import workers
import projects
import tasks
import comments


def abort_forbidden_if_any_condition_not_met(condition_list):
    if not condition_list:
        return None
    elif not condition_list[0]:
        return abort(403)
    else:
        return abort_forbidden_if_any_condition_not_met(condition_list[1:])

def csrf_token_correct():
    return session["csrf_token"] == request.form["csrf_token"]

def worker_id_is_logged_in_worker_id(worker_id):
    return worker_id == session["id"]

def project_manager_id_is_logged_in_worker_id(project_id):
    project = projects.get_one_by_id(project_id)

    return project.manager_id == session["id"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    name = request.form["name"]
    password = request.form["password"]
    retyped_password = request.form["re-typed password"]
    
    error_messages = workers.get_creation_error_messages(name, password, retyped_password)
    if error_messages:
        return render_template("register.html", messages=error_messages)
    
    workers.create(name, password)
    
    workers.login(name, password)

    return redirect("/workers/" + str(session["id"]))

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]
    
    if not workers.get_one_by_name_and_password(name, password):
        return render_template("index.html", message="Incorrect username or password!")
    
    workers.login(name, password)
    
    return redirect("/workers/" + str(session["id"]))

@app.route("/logout", methods=["POST"])
def logout():
    workers.logout()
    
    return redirect("/")

@app.route("/workers/", methods=["GET"])
def workers_list():
    all_workers = workers.get_all()
    
    return render_template("workers.html", workers=all_workers)

@app.route("/workers/<int:id>", methods=["GET"])
def worker(id):
    worker = workers.get_one_by_id(id)

    if not worker:
        return redirect("/")
    
    workers_projects = projects.get_all_by_worker_id(id)
    
    return render_template("worker.html", worker=worker, projects=workers_projects)

@app.route("/workers/<int:worker_id>/resign", methods=["POST"])
def worker_resignation(worker_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), worker_id_is_logged_in_worker_id(worker_id)])

    workers.hide_one_by_id(worker_id)
    projects.remove_worker_from_all_projects(worker_id)

    return redirect("/logout")

@app.route("/projects/<int:project_id>/change_manager/<int:worker_id>", methods=["POST"])
def change_project_manager(project_id, worker_id):
    abort_forbidden_if_any_condition_not_met([csrf_token_correct()])
    projects.change_manager(project_id, worker_id)

    return redirect("/projects/" + str(project_id))

@app.route("/projects/<int:project_id>/add_task", methods=["POST"])
def add_task_to_project(project_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), project_manager_id_is_logged_in_worker_id(project_id)])

    name = request.form["name"]
    description = request.form["description"]
    tasks.create(project_id, name, description)
    
    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/remove", methods=["POST"])
def remove_task_from_project(project_id, task_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), project_manager_id_is_logged_in_worker_id(project_id)])

    tasks.remove_by_id(task_id)
    
    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:id>", methods=["GET"])
def project(id):
    project = projects.get_one_by_id(id)
    if not project:
        return redirect("/")

    project_workers = workers.get_all_by_project_id(id)
    available_workers = workers.get_all_not_in_project_by_project_id(id)

    project_tasks = tasks.get_all_by_project_id(id)
    all_tasks_comments = {}
    for task in project_tasks:
        tasks_comments = comments.get_all_by_task_id(task.id)
        comments_with_authors = []
        for comment in tasks_comments:
            comments_with_authors.append((workers.get_one_by_id(comment.worker_id), comment))

        all_tasks_comments[task.id] = comments_with_authors

    return render_template("project.html", project=project, tasks=project_tasks,
                            available_workers=available_workers, project_workers=project_workers,
                            comments = all_tasks_comments)

@app.route("/projects/<int:project_id>/add_worker/<int:worker_id>", methods=["POST"])
def add_worker_to_project(project_id, worker_id):
    abort_forbidden_if_any_condition_not_met([csrf_token_correct()])

    project = projects.get_one_by_id(project_id)
    worker = workers.get_one_by_id(worker_id)
    if project and worker:
        projects.add_worker_to_project(project_id, worker_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/remove_worker/<int:worker_id>", methods=["POST"])
def remove_worker_from_project(project_id, worker_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), project_manager_id_is_logged_in_worker_id(project_id)])

    project_member_id = projects.get_project_member_id_by_project_id_and_worker_id(project_id, worker_id)
    if project_member_id:
        projects.remove_worker_from_project(project_member_id.id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects", methods=["GET"])
def manage_projects():
    all_projects = projects.get_all()
    return render_template("projects.html", projects=all_projects)

@app.route("/create_project", methods=["POST"])
def create_project():
    abort_forbidden_if_any_condition_not_met([csrf_token_correct()])

    name = request.form["name"]
    error_messages = projects.get_creation_error_messages(name)
    if error_messages:
        all_projects = projects.get_all()
        return render_template("projects.html", projects=all_projects,
                               messages=error_messages)
    projects.create(name)
    return redirect("/projects")

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/add_comment", methods=["POST"])
def add_comment_to_task(project_id, task_id):
    abort_forbidden_if_any_condition_not_met([csrf_token_correct()])

    content = request.form["content"]
    worker_id = session["id"]
    comments.create(task_id, worker_id, content)

    return redirect("/projects/"+str(project_id))
