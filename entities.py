class Project:
    def __init__(self, name, tasks=None):
        self.name = name
        self.tasks = tasks
        self.workers = []

class Task:
    def __init__(self, description, status, deadline):
        self.description = description
        self.status = status
        self.deadline = deadline

class Worker:
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        self.is_supervisor = False