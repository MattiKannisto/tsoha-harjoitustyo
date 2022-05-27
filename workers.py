from xmlrpc.client import boolean
import secrets

from flask import session

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


def login(name, password):
    logged_in_worker = get_one_by_name_and_password(name, password)
    if logged_in_worker:
        session["id"] = logged_in_worker.id
        session["name"] = logged_in_worker.name
        session["csrf_token"] = secrets.token_hex(16)

def logout():
    del session["id"]
    del session["name"]
    del session["csrf_token"]

def get_creation_error_messages(name, password, retyped_password):
    error_messages = get_worker_name_error_messages([], name)
    error_messages = get_passwords_dont_match_error_message(error_messages, password, retyped_password)
    error_messages = get_password_error_message(error_messages, password)
    return error_messages

def get_worker_name_error_messages(error_messages, name):
    if len(name) < 3:
        error_messages.append("Name needs to be at least 3 characters!")
    if len(name) >= 30:
        error_messages.append("Name cannot be over 30 characters!")
    if get_one_by_name(name):
        error_messages.append("Username already taken, please choose another one!")
    return error_messages

def get_passwords_dont_match_error_message(error_messages, password, retyped_password):
    if password != retyped_password:
        error_messages.append("Passwords do not match!")        
    return error_messages

def get_password_error_message(error_messages, password):
    if len(password) < 8:
        error_messages.append("Password needs to be at least 8 characters!")
    if len(password) >= 30:
        error_messages.append("Password cannot be over 30 characters!")
    return error_messages

def create(name, password):
    hashed_password = generate_password_hash(password)
    sql = "INSERT INTO workers (name, password, visible) VALUES (:name, :password, TRUE)"
    db.session.execute(sql, {"name":name, "password":hashed_password})
    db.session.commit()

def hide_one_by_id(id):
    sql = "UPDATE workers SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_one_by_name(name):
    sql = "SELECT id, name FROM workers WHERE name=:name AND visible=TRUE"
    return db.session.execute(sql, {"name":name}).fetchone()

def get_one_by_name_and_password(name, password):
    sql = "SELECT id, name, password FROM workers WHERE name=:name AND visible=TRUE"
    result = db.session.execute(sql, {"name":name}).fetchone()
    if result and check_password_hash(result.password, password):
        return result
    return None

def get_one_by_id(id):
    sql = "SELECT id, name FROM workers WHERE id=:id AND visible=TRUE"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

def get_all():
    sql = "SELECT id, name FROM workers WHERE visible=TRUE"
    return db.session.execute(sql).fetchall()

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
