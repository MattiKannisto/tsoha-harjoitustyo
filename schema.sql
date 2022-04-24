CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    priority INTEGER
);

CREATE TABLE workers (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams,
    project_id INTEGER REFERENCES projects,
    name TEXT UNIQUE,
    password TEXT,
    performance INTEGER,
    is_supervisor BOOLEAN
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects,
    name TEXT,
    description TEXT,
    status TEXT,
    deadline DATE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER REFERENCES workers,
    task_id INTEGER REFERENCES tasks,
    content TEXT,
    date_and_time TIMESTAMP
);