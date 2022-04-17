from typing import Iterable
from xmlrpc.client import boolean

from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from app import db

def head(_list: list) -> list:
    if isinstance(_list, Iterable):
        return _list[:1]
    return None

def tail(_list: list) -> list:
    if isinstance(_list, Iterable):
        return _list[1:]
    return None

def elem(_list: list, element) -> bool:
    if not _list:
        return False
    if head(_list) == [element]:
        return True
    return elem(tail(_list), element)

def get_worker_creation_error_messages(name: str, password: str, retyped_password: str) -> list:
    error_messages = get_worker_name_error_messages([], name)
    error_messages = get_passwords_dont_match_error_message(error_messages, password, retyped_password)
    error_messages = get_password_error_message(error_messages, password)
    return error_messages

def get_worker_name_error_messages(error_messages, name):
    if len(name) < 3:
        error_messages.append("Name needs to be at least 3 characters!")
    if len(name) >= 30:
        error_messages.append("Name cannot be over characters!")
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

def valid_password(password):
    return password == "salasana"

def create_worker(name, password, is_supervisor=False):
    hashed_password = generate_password_hash(password)
    sql = "INSERT INTO worker (name, password, is_supervisor) VALUES (:name, :password, :is_supervisor)"
    db.session.execute(sql, {"name":name, "password":hashed_password, "is_supervisor":is_supervisor})
    db.session.commit()
    
def get_worker_list():
    return db.session.execute("SELECT name FROM worker").fetchall()

def add_workers_to_project(project, workers):
    # Hae projekti databasesta
    if workers:
        project.workers = project.workers + workers
    # Tallenna muokattu projekti databaseen