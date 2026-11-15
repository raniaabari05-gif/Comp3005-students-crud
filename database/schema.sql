-- schema.sql
-- Creates the "students" table exactly as specified in the assignment.
-- Run this against an existing database (e.g. "students_db"):
--     psql -U postgres -d students_db -f database/schema.sql

-- Drop the table first so the script can be re-run cleanly during testing.
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    -- SERIAL = auto-incrementing integer; PRIMARY KEY makes it unique and not null.
    student_id      SERIAL PRIMARY KEY,
    -- Names are required fields.
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    -- Email is required and no two students may share one.
    email           TEXT NOT NULL UNIQUE,
    -- Enrollment date is optional (nullable).
    enrollment_date DATE
);
