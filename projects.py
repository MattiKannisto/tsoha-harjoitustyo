from datetime import datetime

from flask import session

from database import db

TABLE_NAME = "projects"
NAME_MIN_LENGTH = 5
NAME_MAX_LENGTH = 50

def get_one_by_id(project_id):
    sql = "SELECT id, name, manager_id FROM projects WHERE id=:id"
    result = db.session.execute(sql, {"id":project_id}).fetchone()
    return result

def add_worker_to_project(project_id, worker_id):
    contract_start_time = datetime.now().isoformat(' ', 'seconds')

    sql = """INSERT INTO project_members (project_id, worker_id, contract_start_time)
             VALUES (:project_id, :worker_id, :contract_start_time)"""
    db.session.execute(sql, {"project_id":project_id, "worker_id":worker_id,
                             "contract_start_time":contract_start_time})
    db.session.commit()

def remove_worker_from_project(id):
    end_worker_contract(id, "id")

def remove_worker_from_all_projects(id):
    end_worker_contract(id, "worker_id")

def end_worker_contract(id, target_id):
    contract_end_time = datetime.now().isoformat(' ', 'seconds')

    sql = "UPDATE project_members SET contract_end_time=:contract_end_time WHERE " + target_id + "=:id"
    db.session.execute(sql, {"id":id, "contract_end_time":contract_end_time})
    db.session.commit()

def get_project_member_id_by_project_id_and_worker_id(project_id, worker_id):
    sql = """SELECT id FROM project_members WHERE project_id=:project_id AND worker_id=:worker_id
             AND contract_end_time IS NULL"""
    return db.session.execute(sql, {"project_id":project_id, "worker_id":worker_id}).fetchone()

def get_one_by_name(name):
    sql = "SELECT id, name FROM projects WHERE name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()

def change_manager(project_id, manager_id):
    sql = "UPDATE projects SET manager_id=:manager_id WHERE id=:project_id"
    db.session.execute(sql, {"project_id":project_id, "manager_id":manager_id})
    db.session.commit()


def create(name):
    sql = "INSERT INTO projects (name, manager_id) VALUES (:name, :manager_id)"
    db.session.execute(sql, {"name":name, "manager_id":session["id"]})
    db.session.commit()

def get_all_with_tasks_and_workers_info():
    sql = """SELECT id, manager_id, name,
    (SELECT COUNT(*) FROM project_members WHERE project_id=projects.id AND contract_end_time IS NULL) AS current_workers,
    (SELECT COUNT(DISTINCT worker_id) FROM project_members WHERE project_id=projects.id AND contract_end_time IS NOT NULL AND name NOT IN
    (SELECT name FROM project_members WHERE project_id=projects.id AND contract_end_time IS NULL)) AS past_workers,
    (SELECT COUNT(*) FROM tasks WHERE project_id=projects.id AND status='Complete') AS completed_tasks,
    (SELECT COUNT(*) FROM tasks WHERE project_id=projects.id AND status='Incomplete') AS incomplete_tasks,
    (SELECT COUNT(*) FROM tasks WHERE project_id=projects.id AND status='OVERDUE') AS overdue_tasks
    FROM projects"""
    return db.session.execute(sql).fetchall()

def get_all_by_worker_id(worker_id):
    sql = """SELECT p.id, p.manager_id, p.name FROM projects p WHERE p.id IN (
             SELECT p_m.project_id FROM project_members p_m WHERE p_m.worker_id=:worker_id
             AND p_m.contract_end_time IS NULL)"""
    return db.session.execute(sql, {"worker_id":worker_id}).fetchall()

def get_all_with_incomplete_or_overdue_tasks_by_manager_id(manager_id):
    sql = """SELECT id, manager_id, name FROM projects WHERE manager_id=:manager_id AND id IN
             (SELECT project_id FROM tasks WHERE status='Incomplete' OR status='OVERDUE')""" 
    return db.session.execute(sql, {"manager_id":manager_id}).fetchall()
