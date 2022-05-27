from xmlrpc.client import boolean

from datetime import date, timedelta

from database import db

def get_all_by_project_id(id):
    update_statuses_by_project_id(id)

    sql = "SELECT id, name, description, status, deadline FROM tasks WHERE project_id=:id"
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result

def create(project_id, name, description):
#    deadline = date.today()
    deadline = date.today() - timedelta(days=1)
    sql = "INSERT INTO tasks (project_id, name, description, status, deadline) VALUES (:project_id, :name, :description, 'Incomplete', :deadline)"
    db.session.execute(sql, {"project_id":project_id, "name":name, "description":description, "deadline":deadline})
    db.session.commit()

def remove_by_id(id):
    sql = "DELETE FROM tasks WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def update_statuses_by_project_id(project_id):
    today = date.today()
    #print(today)

    sql = "UPDATE tasks SET status='OVERDUE' WHERE project_id=:project_id AND deadline<:today;"
    db.session.execute(sql, {"project_id":project_id, "today":today})
    db.session.commit()
