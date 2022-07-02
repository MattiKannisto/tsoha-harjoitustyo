from datetime import date, datetime

from database import db

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 5
DESCRIPTION_MAX_LENGTH = 500

def valid_date(valided_date):
    try:
        datetime.strptime(valided_date, "%Y-%m-%d").date()
        return True
    except:
        return False

def valid_name_length(name):
    return NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH

def valid_description_length(description):
    return DESCRIPTION_MIN_LENGTH <= len(description) <= DESCRIPTION_MAX_LENGTH

def get_one_by_id_and_project_id(task_id, project_id):
    sql = """SELECT id, name, description, status, deadline FROM tasks WHERE id=:task_id
             AND project_id=:project_id"""
    result = db.session.execute(sql, {"task_id":task_id, "project_id":project_id}).fetchone()
    if result:
        return result
    return None

def get_all_by_status_and_project_id_sort_by_deadline(status, project_id):
    update_overdue_tasks_by_project_id(project_id)
    update_on_time_tasks_by_project_id(project_id)

    sql = """SELECT id, name, description, status, deadline FROM tasks WHERE project_id=:id AND
             status=:status ORDER BY deadline"""
    return db.session.execute(sql, {"id":id, "status": status}).fetchall()

def create(project_id, name, description, deadline):
    if valid_name_length(name) and valid_description_length(description) and valid_date(deadline):
        sql = """INSERT INTO tasks (project_id, name, description, status, deadline) VALUES
                 (:project_id, :name, :description, 'Incomplete', :deadline)"""
        db.session.execute(sql, {"project_id":project_id, "name":name, "description":description,
                                 "deadline":deadline})
        db.session.commit()

def remove_by_id(task_id):
    sql = "DELETE FROM tasks WHERE id=:id"
    db.session.execute(sql, {"id":task_id})
    db.session.commit()

def update_overdue_tasks_by_project_id(project_id):
    today = date.today()

    sql = """UPDATE tasks SET status='OVERDUE' WHERE project_id=:project_id AND deadline<:today
             AND status='Incomplete';"""
    db.session.execute(sql, {"project_id":project_id, "today":today})
    db.session.commit()

def update_on_time_tasks_by_project_id(project_id):
    today = date.today()

    sql = """UPDATE tasks SET status='Incomplete' WHERE project_id=:project_id AND deadline>=:today
             AND status='OVERDUE';"""
    db.session.execute(sql, {"project_id":project_id, "today":today})
    db.session.commit()

def update_deadline_by_id(task_id, deadline):
    if valid_date(deadline):
        sql = "UPDATE tasks SET deadline=:deadline WHERE id=:task_id;"
        db.session.execute(sql, {"task_id":task_id, "deadline":deadline})
        db.session.commit()

def set_status_completed(task_id):
    sql = "UPDATE tasks SET status='Completed' WHERE id=:task_id"
    db.session.execute(sql, {"task_id":task_id})
    db.session.commit()
