CREATE TABLE workers (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    visible BOOLEAN
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER REFERENCES workers,
    name TEXT UNIQUE
);

CREATE TABLE project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects ON DELETE CASCADE,
    worker_id INTEGER REFERENCES workers ON DELETE CASCADE,
    contract_start_time TIMESTAMP,
    contract_end_time TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects ON DELETE CASCADE,
    name TEXT,
    description TEXT,
    status TEXT,
    deadline DATE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER REFERENCES workers,
    task_id INTEGER REFERENCES tasks ON DELETE CASCADE,
    content TEXT,
    date_and_time TIMESTAMP
);
