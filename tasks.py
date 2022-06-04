from xmlrpc.client import boolean

from datetime import date, timedelta

from database import db

TABLE_NAME = "tasks"
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 5
DESCRIPTION_MAX_LENGTH = 500

def get_all_by_project_id(id):
    update_overdue_tasks_by_project_id(id)
    update_on_time_tasks_by_project_id(id)

    sql = "SELECT id, name, description, status, deadline FROM tasks WHERE project_id=:id"
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result

def create(project_id, name, description, deadline):
    sql = "INSERT INTO tasks (project_id, name, description, status, deadline) VALUES (:project_id, :name, :description, 'Incomplete', :deadline)"
    db.session.execute(sql, {"project_id":project_id, "name":name, "description":description, "deadline":deadline})
    db.session.commit()

def remove_by_id(id):
    sql = "DELETE FROM tasks WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def update_overdue_tasks_by_project_id(project_id):
    today = date.today()

    sql = "UPDATE tasks SET status='OVERDUE' WHERE project_id=:project_id AND deadline<:today;"
    db.session.execute(sql, {"project_id":project_id, "today":today})
    db.session.commit()

def update_on_time_tasks_by_project_id(project_id):
    today = date.today()

    sql = "UPDATE tasks SET status='Incomplete' WHERE project_id=:project_id AND deadline>=:today;"
    db.session.execute(sql, {"project_id":project_id, "today":today})
    db.session.commit()

def update_deadline_by_id(task_id, deadline):
    sql = "UPDATE tasks SET deadline=:deadline WHERE id=:task_id;"
    db.session.execute(sql, {"task_id":task_id, "deadline":deadline})
    db.session.commit()
