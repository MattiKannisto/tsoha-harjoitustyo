import secrets

from flask import session

from werkzeug.security import check_password_hash, generate_password_hash

from database import db

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 40

def valid_name_length(name):
    return NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH

def valid_password_length(password):
    return PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH

def login(name, password):
    logged_in_worker = get_one_by_name_and_password(name, password)
    if logged_in_worker:
        session["id"] = logged_in_worker.id
        session["name"] = logged_in_worker.name
        session["csrf_token"] = secrets.token_hex(16)
        session["general_error_message"] = None
        if session.get("login_error_message"):
            del session["login_error_message"]

def logout():
    del session["id"]
    del session["name"]
    del session["csrf_token"]
    if session.get("general_error_message"):
        del session["general_error_message"]

def get_login_error_message(name, password):
    if session.get("name") and not get_one_by_name_and_password(name, password):
        return "Incorrect password!"
    if not get_one_by_name_and_password(name, password):
        return "Incorrect username or password!"
    return None

def create(name, password):
    if not get_one_by_name(name) and valid_name_length(name) and valid_password_length(password):
        hashed_password = generate_password_hash(password)
        sql = "INSERT INTO workers (name, password, visible) VALUES (:name, :password, TRUE)"
        db.session.execute(sql, {"name":name, "password":hashed_password})
        db.session.commit()

def hide_one_by_id(worker_id):
    sql = "UPDATE workers SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":worker_id})
    db.session.commit()

def get_one_by_name(name):
    sql = "SELECT id, name FROM workers WHERE name=:name AND visible=TRUE"
    return db.session.execute(sql, {"name":name}).fetchone()

def get_username_already_taken_error_message(name):
    if get_one_by_name(name):
        return "Username already taken, please choose another one!"
    return None

def get_one_by_name_and_password(name, password):
    sql = "SELECT id, name, password FROM workers WHERE name=:name AND visible=TRUE"
    result = db.session.execute(sql, {"name":name}).fetchone()
    if result and check_password_hash(result.password, password):
        return result
    return None

def get_one_by_id(worker_id):
    sql = "SELECT id, name FROM workers WHERE id=:id AND visible=TRUE"
    return db.session.execute(sql, {"id":worker_id}).fetchone()

def get_all_by_project_id(project_id):
    sql = """SELECT w.id, w.name FROM workers w WHERE w.id IN (
             SELECT p_m.worker_id FROM project_members p_m WHERE p_m.project_id=:project_id
             AND p_m.contract_end_time IS NULL
    ) AND w.visible=TRUE"""
    return db.session.execute(sql, {"project_id":project_id}).fetchall()

def get_all_not_in_project_by_project_id(project_id):
    sql = """SELECT w.id, w.name FROM workers w WHERE w.id NOT IN (
             SELECT p_m.worker_id FROM project_members p_m WHERE p_m.project_id=:project_id
             AND p_m.contract_end_time IS NULL
    ) AND w.visible=TRUE"""
    return db.session.execute(sql, {"project_id":project_id}).fetchall()

def get_all_with_projects_tasks_and_comments_info():
    sql = """SELECT id, name,
    (SELECT COUNT(*) FROM project_members WHERE worker_id=workers.id AND contract_end_time IS NULL) AS projects,
    (SELECT COUNT(*) FROM projects WHERE manager_id=workers.id) AS managed_projects,
    (SELECT COUNT(*) FROM tasks WHERE status='Complete' AND project_id IN 
    (SELECT project_id FROM project_members WHERE worker_id=workers.id AND contract_end_time IS NULL)) AS completed_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status='Incomplete' AND project_id IN 
    (SELECT project_id FROM project_members WHERE worker_id=workers.id AND contract_end_time IS NULL)) AS incomplete_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status='OVERDUE' AND project_id IN 
    (SELECT project_id FROM project_members WHERE worker_id=workers.id AND contract_end_time IS NULL)) AS overdue_tasks
    FROM workers WHERE visible=TRUE"""
    return db.session.execute(sql).fetchall()
