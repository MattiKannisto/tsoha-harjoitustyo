from flask import redirect, render_template, session, request, abort

from app import app
import workers
import projects
import tasks
import comments


def abort_forbidden_if_any_is_false(condition_list):
    if not condition_list:
        return None
    if not condition_list[0]:
        return abort(403)
    return abort_forbidden_if_any_is_false(condition_list[1:])

def csrf_token_correct():
    return session["csrf_token"] == request.form["csrf_token"]

def worker_id_is_logged_in_worker_id(worker_id):
    return worker_id == session["id"]

def project_manager_id_is_logged_in_worker_id(project_id):
    project = projects.get_one_by_id(project_id)

    return project.manager_id == session["id"]

def worker_works_in_the_project(worker_id, project_id):
    return (projects.get_project_member_id_by_project_id_and_worker_id(project_id, worker_id)
            is not None)

def task_belongs_to_project(task_id, project_id):
    return tasks.get_one_by_id_and_project_id(task_id, project_id) is not None

def user_logged_in():
    return session.get("id") is not None

def extract_session_value(key):
    value = session.get(key)
    session[key] = None
    return value

def is_logged_in_user_project_worker_or_manager(project_id, project):
    if not session.get('id'):
        return False
    return (projects.get_project_member_id_by_project_id_and_worker_id(project_id, session['id'])
            or session['id'] is project.manager_id)

@app.route("/")
def index():
    return render_template("index.html",
                           login_error_message=extract_session_value("login_error_message"),
                           error_message=extract_session_value("error_message"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if user_logged_in():
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html",
                               login_error_message=extract_session_value("login_error_message"),
                               error_message=extract_session_value("error_message"),
                               name_min_length=workers.NAME_MIN_LENGTH,
                               name_max_length=workers.NAME_MAX_LENGTH,
                               password_min_length=workers.PASSWORD_MIN_LENGTH,
                               password_max_length=workers.PASSWORD_MAX_LENGTH)

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        session["error_message"] = workers.get_username_already_taken_error_message(name)

        if not session["error_message"]:
            workers.create(name, password)
            workers.login(name, password)

        return redirect(request.referrer)

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]

    session["login_error_message"] = workers.get_login_error_message(name, password)

    workers.login(name, password)

    return redirect(request.referrer)

@app.route("/logout", methods=["POST"])
def logout():
    workers.logout()

    return redirect(request.referrer)

@app.route("/workers/", methods=["GET"])
def workers_list():
    return render_template("workers.html",
                           login_error_message=extract_session_value("login_error_message"),
                           error_message=extract_session_value("error_message"),
                           workers=workers.get_all_with_projects_tasks_and_comments_info())

@app.route("/resign", methods=["GET", "POST"])
def worker_resignation():
    worker_id = session.get("id")
    managed_incomplete_projects = projects.get_all_incomplete_projects_by_manager_id(worker_id)

    if not worker_id:
        return redirect("/")

    if request.method == "POST":
        abort_forbidden_if_any_is_false([csrf_token_correct()])

        password = request.form["password"]

        if managed_incomplete_projects:
            session["error_message"] = """Please assign new project managers to your projects
                                       or remove the projects first!"""
        else:
            session["error_message"] = workers.get_login_error_message(session["name"], password)

        if not session["error_message"]:
            workers.hide_one_by_id(worker_id)
            projects.remove_worker_from_all_projects(worker_id)
            workers.logout()

            return redirect("/")

    return render_template("resign.html",
                           error_message=extract_session_value("error_message"),
                           incomplete_projects=managed_incomplete_projects)

@app.route("/projects/<int:project_id>/change_manager/<int:worker_id>", methods=["POST"])
def change_project_manager(project_id, worker_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id),
                                     worker_works_in_the_project(worker_id, project_id)])

    projects.change_manager(project_id, worker_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/add_task", methods=["POST"])
def add_task_to_project(project_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id)])

    tasks.create(project_id, request.form["name"], request.form["description"],
                 request.form["deadline"])

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/remove", methods=["POST"])
def remove_task_from_project(project_id, task_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id),
                                     task_belongs_to_project(task_id, project_id)])

    tasks.remove_by_id(task_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/change_deadline", methods=["POST"])
def change_task_deadline(project_id, task_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id),
                                     task_belongs_to_project(task_id, project_id)])

    tasks.update_deadline_by_id(task_id, request.form["deadline"])

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/set_status_completed", methods=["POST"])
def set_task_status_completed(project_id, task_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id),
                                     task_belongs_to_project(task_id, project_id)])

    tasks.set_status_completed(task_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>", methods=["GET"])
def single_project(project_id):
    project = projects.get_one_by_id(project_id)

    if project:
        return render_template("project.html",
                               project=project,
                               login_error_message=extract_session_value("login_error_message"),
                               error_message=extract_session_value("error_message"),
                               overdue_tasks=
                               tasks.get_all_by_status_and_project_id_sort_by_deadline('OVERDUE',
                                                                                       project_id),
                               incomplete_tasks=
                               tasks.get_all_by_status_and_project_id_sort_by_deadline('Incomplete',
                                                                                       project_id),
                               completed_tasks=
                               tasks.get_all_by_status_and_project_id_sort_by_deadline('Completed',
                                                                                       project_id),
                               comments=comments.get_all_with_authors_by_project_id(project_id),
                               project_manager=workers.get_one_by_id(project.manager_id),
                               logged_in_user_project_worker_or_manager=
                               is_logged_in_user_project_worker_or_manager(project_id, project),
                               available_workers=
                               workers.get_all_not_in_project_by_project_id(project_id),
                               project_workers=
                               workers.get_all_by_project_id(project_id),
                               comment_content_min_length=comments.CONTENT_MIN_LENGTH,
                               comment_content_max_length=comments.CONTENT_MAX_LENGTH,
                               task_name_min_length=tasks.NAME_MIN_LENGTH,
                               task_name_max_length=tasks.NAME_MAX_LENGTH,
                               task_description_min_length=tasks.DESCRIPTION_MIN_LENGTH,
                               task_description_max_length=tasks.DESCRIPTION_MAX_LENGTH)

    return redirect("/")

@app.route("/projects/<int:project_id>/add_worker", methods=["POST"])
def add_worker_to_project(project_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id)])

    worker_id = request.form.get("worker_id")

    if workers.get_one_by_id(worker_id):
        projects.add_worker_to_project(project_id, worker_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects/<int:project_id>/remove_worker/<int:worker_id>", methods=["POST"])
def remove_worker_from_project(project_id, worker_id):
    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     project_manager_id_is_logged_in_worker_id(project_id),
                                     worker_works_in_the_project(worker_id, project_id)])

    projects.remove_worker_from_project(project_id, worker_id)

    return redirect("/projects/"+str(project_id))

@app.route("/projects", methods=["GET", "POST"])
def all_projects():
    if request.method == "GET":
        return render_template("projects.html",
                               login_error_message=extract_session_value("login_error_message"),
                               error_message=extract_session_value("error_message"),
                               projects=projects.get_all_latest_first_with_task_and_worker_info(),
                               name_min_length=projects.NAME_MIN_LENGTH,
                               name_max_length=projects.NAME_MAX_LENGTH)

    if request.method == "POST":
        abort_forbidden_if_any_is_false([csrf_token_correct()])

        name = request.form["name"]

        session["error_message"] = projects.get_project_name_already_in_use_error_message(name)

        projects.create(name)

        return redirect("/projects")

@app.route("/projects/<int:project_id>/tasks/<int:task_id>/add_comment", methods=["POST"])
def add_comment_to_task(project_id, task_id):
    worker_id = session["id"]

    abort_forbidden_if_any_is_false([csrf_token_correct(),
                                     worker_works_in_the_project(worker_id, project_id),
                                     task_belongs_to_project(task_id, project_id)])

    comments.create(task_id, worker_id, request.form["content"])

    return redirect("/projects/"+str(project_id))
