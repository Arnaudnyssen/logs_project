-- Create table if not exists for cpu
CREATE TABLE IF NOT EXISTS cpu (
    id SERIAL PRIMARY KEY,
    date DATE,
    hour INT,
    minute INT,
    cpu_percent FLOAT
);


-- Create table if not exists for memory
CREATE TABLE IF NOT EXISTS memory (
    id SERIAL PRIMARY KEY,
    date DATE,
    hour INT,
    minute INT,
    available_gb FLOAT,
    percent_used FLOAT
);
