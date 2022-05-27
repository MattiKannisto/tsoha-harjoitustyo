from datetime import datetime

from database import db

def create(task_id, worker_id, content):
    date_and_time = datetime.now().isoformat(' ', 'seconds')

    sql = """INSERT INTO comments (task_id, worker_id, content, date_and_time) VALUES
             (:task_id, :worker_id, :content, :date_and_time)"""
    db.session.execute(sql, {"task_id":task_id, "worker_id":worker_id,
                       "content":content, "date_and_time":date_and_time})
    db.session.commit()

def get_all_by_task_id(task_id):
    sql = "SELECT id, worker_id, task_id, content, date_and_time FROM comments WHERE task_id=:id"
    result = db.session.execute(sql, {"id":task_id}).fetchall()
    return result
