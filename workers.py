from xmlrpc.client import boolean

from werkzeug.security import check_password_hash, generate_password_hash

from database import db

def get_worker_creation_error_messages(name: str, password: str, retyped_password: str) -> list:
    error_messages = get_worker_name_error_messages([], name)
    error_messages = get_passwords_dont_match_error_message(error_messages, password, retyped_password)
    error_messages = get_password_error_message(error_messages, password)
    return error_messages

def get_worker_name_error_messages(error_messages, name):
    if len(name) < 3:
        error_messages.append("Name needs to be at least 3 characters!")
    if len(name) >= 30:
        error_messages.append("Name cannot be over 30 characters!")
    if get_worker_by_name(name):
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

def create_worker(name, password, is_supervisor=False):
    hashed_password = generate_password_hash(password)
    sql = "INSERT INTO workers (name, password, performance, is_supervisor) VALUES (:name, :password, :performance, :is_supervisor)"
    db.session.execute(sql, {"name":name, "password":hashed_password, "performance":0, "is_supervisor":is_supervisor})
    db.session.commit()

def remove_worker(id):
    sql = "DELETE FROM workers WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_worker_by_name(name):
    sql = "SELECT id, name, password, is_supervisor FROM workers WHERE name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()

def get_worker_by_name_and_password(name, password):
    sql = "SELECT id, name, password, is_supervisor FROM workers WHERE name=:name"
    result = db.session.execute(sql, {"name":name}).fetchone()
    if result and check_password_hash(result.password, password):
        return result
    return None

def get_worker_name_by_id(id):
    sql = "SELECT name FROM workers WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result.name

def get_worker_by_id(id):
    sql = "SELECT id, name FROM workers WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

def get_all_workers():
    sql = "SELECT id, name FROM workers"
    return db.session.execute(sql).fetchall()

def get_all_free_workers():
    sql = "SELECT id, name FROM workers WHERE project_id is NULL"
    return db.session.execute(sql).fetchall()

def get_worker_supervisor_status_by_id(id):
    sql = "SELECT is_supervisor FROM workers WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result.is_supervisor

def get_workers_by_project_id(id):
    sql = "SELECT id, name FROM workers WHERE project_id=:id"
    return db.session.execute(sql, {"id":id}).fetchall()
    
def get_supervisors_sorted_by_seniority():
    sql = "SELECT id FROM workers WHERE is_supervisor=TRUE ORDER BY id DESC"
    return db.session.execute(sql).fetchall()

def grant_supervisor_status(id):
    if get_worker_name_by_id(id):
        sql = "UPDATE workers SET is_supervisor=TRUE WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()

def remove_supervisor_status(id):
    if get_worker_name_by_id(id):
        sql = "UPDATE workers SET is_supervisor=FALSE WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
