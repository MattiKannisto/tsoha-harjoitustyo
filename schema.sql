CREATE TABLE worker (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    is_supervisor BOOLEAN
);

CREATE TABLE project (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    description TEXT,
    status TEXT,
    deadline DATE
);
