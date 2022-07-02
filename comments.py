from datetime import datetime

from database import db

CONTENT_MIN_LENGTH = 2
CONTENT_MAX_LENGTH = 100

def valid_content_length(content):
    return CONTENT_MIN_LENGTH <= len(content) <= CONTENT_MAX_LENGTH

def create(task_id, worker_id, content):
    if valid_content_length(content):
        date_and_time = datetime.now().isoformat(' ', 'seconds')

        sql = """INSERT INTO comments (task_id, worker_id, content, date_and_time) VALUES
                (:task_id, :worker_id, :content, :date_and_time)"""
        db.session.execute(sql, {"task_id":task_id, "worker_id":worker_id,
                                 "content":content, "date_and_time":date_and_time})
        db.session.commit()

def get_all_with_authors_by_project_id(project_id):
    sql = """SELECT id, (SELECT name FROM workers WHERE id=comments.worker_id) AS author, task_id,
             content, date_and_time FROM comments WHERE task_id IN
             (SELECT id FROM tasks WHERE project_id=:project_id)"""
    return db.session.execute(sql, {"project_id":project_id}).fetchall()
