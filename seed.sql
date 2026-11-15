-- seed.sql
-- Populates the "students" table with the initial data from the assignment.
-- Run AFTER schema.sql:
--     psql -U postgres -d students_db -f database/seed.sql

-- student_id is omitted so PostgreSQL assigns it automatically (1, 2, 3).
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe',   'john.doe@example.com',   '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim',  'Beam',  'jim.beam@example.com',   '2023-09-02');
