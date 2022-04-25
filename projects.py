from database import db

def get_project_by_id(id):
    sql = "SELECT id, name FROM projects WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

def get_project_by_name(name):
    sql = "SELECT id, name FROM projects WHERE name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()

def get_project_creation_error_messages(name):
    error_messages = get_project_name_error_messages(name)
    return error_messages

def get_project_name_error_messages(name):
    if get_project_by_name(name):
        return ["Project name already taken, please choose another one!"]

def save_project(name):
    sql = "INSERT INTO projects (name) VALUES (:name)"
    db.session.execute(sql, {"name":name})
    db.session.commit()

def get_all_projects():
    sql = "SELECT id, name FROM projects"
    return db.session.execute(sql).fetchall()

def add_worker_to_project(project_id, worker_id):
    if get_project_by_id(project_id):
        sql = "UPDATE workers SET project_id=:project_id WHERE id=:worker_id"
        db.session.execute(sql, {"project_id":project_id, "worker_id":worker_id})
        db.session.commit()
