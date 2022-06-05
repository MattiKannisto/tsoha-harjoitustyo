from flask import redirect, render_template, session, request, abort

import datetime

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

def valid_date(valided_date):
    try:
        date_in_valid_format = datetime.datetime.strptime(valided_date, "%Y-%m-%d").date()
        return True
    except:
        return False

def extract_session_value(key):
    value = session.get(key)
    session[key] = None
    return value

@app.route("/")
def index():
    return render_template("index.html", login_error_message=extract_session_value("login_error_message"),
                          general_error_message=extract_session_value("general_error_message"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", login_error_message=extract_session_value("login_error_message"),
                                general_error_message=extract_session_value("general_error_message"),
                                name_min_length=workers.NAME_MIN_LENGTH,
                                name_max_length=workers.NAME_MAX_LENGTH,
                                password_min_length=workers.PASSWORD_MIN_LENGTH,
                                password_max_length=workers.PASSWORD_MAX_LENGTH)

    
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        
        if workers.get_one_by_name(name):
            session["general_error_message"] = "Username already taken, please choose another one!"
            return redirect(request.referrer)

        workers.create(name, password)
        workers.login(name, password)

        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]

    if not workers.get_one_by_name_and_password(name, password):
        session["login_error_message"] = "Incorrect username or password!"
    else:
        workers.login(name, password)
    
    return redirect(request.referrer)

@app.route("/logout", methods=["POST"])
def logout():
    workers.logout()
    
    return redirect(request.referrer)

@app.route("/workers/", methods=["GET"])
def workers_list():
    all_workers = workers.get_all_with_projects_tasks_and_comments_info()
    
    return render_template("workers.html",login_error_message=extract_session_value("login_error_message"),
                          general_error_message=extract_session_value("general_error_message"), workers=all_workers)

@app.route("/workers/<int:id>", methods=["GET"])
def worker(id):
    worker = workers.get_one_by_id(id)

    if not worker:
        return redirect(request.referrer)
    
    workers_projects = projects.get_all_by_worker_id(id)
    
    return render_template("worker.html", login_error_message=extract_session_value("login_error_message"),
                          general_error_message=extract_session_value("general_error_message"),
                          worker=worker, projects=workers_projects)

@app.route("/resign", methods=["GET", "POST"])
def worker_resignation():
    worker_id = session.get("id")
    managed_projects = projects.get_all_by_manager_id(worker_id)

    if not worker_id:
        return redirect("/")

    if request.method == "POST":
        abort_forbidden_if_any_condition_not_met(
            [csrf_token_correct()])

        password = request.form["password"]

        if managed_projects:
            session["general_error_message"] = "Please assign new project managers to your projects or remove the projects first!"
        elif not workers.get_one_by_name_and_password(session["name"], password):
            session["general_error_message"] = "Incorrect password!"
        else:
            workers.hide_one_by_id(worker_id)
            projects.remove_worker_from_all_projects(worker_id)
            workers.logout()

            return redirect("/")

    return render_template("resign.html",
                          general_error_message=extract_session_value("general_error_message"),
                          projects=managed_projects)


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
    deadline = request.form["deadline"]
    # Tarkistus että on validi päivämäärä yms. tarkistukset
    if valid_date(deadline):
        tasks.create(project_id, name, description, deadline)
    
    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/remove", methods=["POST"])
def remove_task_from_project(project_id, task_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), project_manager_id_is_logged_in_worker_id(project_id)])

    tasks.remove_by_id(task_id)
    
    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/change_deadline", methods=["POST"])
def change_task_deadline(project_id, task_id):
    abort_forbidden_if_any_condition_not_met(
        [csrf_token_correct(), project_manager_id_is_logged_in_worker_id(project_id)]) # task_belongs_to_project(task_id, project_id)

    deadline = request.form["deadline"]
    if valid_date(deadline):
        tasks.update_deadline_by_id(task_id, deadline)
    
    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:id>", methods=["GET"])
def project(id):
    project = projects.get_one_by_id(id)
    if not project:
        return redirect("/")

    project_workers = workers.get_all_by_project_id(id)
    available_workers = workers.get_all_not_in_project_by_project_id(id)
    project_tasks = tasks.get_all_by_project_id(id)
    project_tasks_comments = comments.get_all_with_authors_by_project_id(id)

    return render_template("project.html", project=project, login_error_message=extract_session_value("login_error_message"),
                          general_error_message=extract_session_value("general_error_message"),
                          tasks=project_tasks, comments = project_tasks_comments,
                            available_workers=available_workers, project_workers=project_workers,
                            comment_content_min_length=comments.CONTENT_MIN_LENGTH,
                            comment_content_max_length=comments.CONTENT_MAX_LENGTH, task_name_min_length=
                            tasks.NAME_MIN_LENGTH, task_name_max_length=tasks.NAME_MAX_LENGTH,
                            task_description_min_length=tasks.DESCRIPTION_MIN_LENGTH, task_description_max_length=
                            tasks.DESCRIPTION_MAX_LENGTH)

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

@app.route("/projects", methods=["GET", "POST"])
def all_projects():
    if request.method == "GET":
        all_projects_with_tasks_and_workers = projects.get_all_with_tasks_and_workers_info()
        return render_template("projects.html", login_error_message=extract_session_value("login_error_message"),
                          general_error_message=extract_session_value("general_error_message"),
                          projects=all_projects_with_tasks_and_workers,
                                name_min_length=projects.NAME_MIN_LENGTH,
                                name_max_length=projects.NAME_MAX_LENGTH)

    if request.method == "POST":
        abort_forbidden_if_any_condition_not_met([csrf_token_correct()])

        name = request.form["name"]

        if projects.get_one_by_name(name):
            session["general_error_message"] = "Project name already taken, please choose another one!"
        else:
            projects.create(name)

        return redirect("/projects")

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/add_comment", methods=["POST"])
def add_comment_to_task(project_id, task_id):
    abort_forbidden_if_any_condition_not_met([csrf_token_correct()])

    content = request.form["content"]
    worker_id = session["id"]

    if comments.correct_length(content):
        comments.create(task_id, worker_id, content)

    return redirect("/projects/"+str(project_id))
