# PostgreSQL Students Database – CRUD Application

A Python command-line app that connects to a PostgreSQL database and performs
Create, Read, Update and Delete operations on a `students` table.

**Demo video:** <PASTE VIDEO LINK HERE>

## Repository structure

```
.
├── database/
│   ├── schema.sql        # creates the students table
│   └── seed.sql          # inserts the 3 initial students
├── app/
│   ├── students_app.py   # application with the 4 CRUD functions + menu
│   └── requirements.txt  # Python dependency (psycopg2)
└── README.md
```

## Prerequisites

- PostgreSQL (tested with 16) and pgAdmin 4
- Python 3.8+

## 1. Set up the database

**Using pgAdmin**

1. Right-click **Databases → Create → Database…**, name it `students_db`, and save.
2. Select `students_db`, open **Tools → Query Tool**.
3. Open `database/schema.sql`, run it (F5).
4. Open `database/seed.sql`, run it (F5).
5. Check: right-click **students_db → Schemas → public → Tables → students → View/Edit Data → All Rows**. You should see 3 rows.

**Or using psql**

```bash
createdb -U postgres students_db
psql -U postgres -d students_db -f database/schema.sql
psql -U postgres -d students_db -f database/seed.sql
```

## 2. Install the Python dependency

```bash
cd app
pip install -r requirements.txt
```

## 3. Configure the connection

The app reads standard PostgreSQL environment variables. Defaults are shown;
set only the ones that differ on your machine (usually just the password).

| Variable     | Default       |
|--------------|---------------|
| `PGHOST`     | `localhost`   |
| `PGPORT`     | `5432`        |
| `PGDATABASE` | `students_db` |
| `PGUSER`     | `postgres`    |
| `PGPASSWORD` | `postgres`    |

```bash
# macOS / Linux
export PGPASSWORD=your_password

# Windows (PowerShell)
$env:PGPASSWORD="your_password"
```

## 4. Run the application

Python is interpreted, so there is no compile step.

```bash
python students_app.py
```

A menu appears:

```
=== Students Database ===
1. View all students
2. Add a student
3. Update a student's email
4. Delete a student
5. Exit
```

## Functions

| Function | Operation | What it does |
|---|---|---|
| `getAllStudents()` | Read | Selects all rows ordered by `student_id` and prints them as a table. |
| `addStudent(first_name, last_name, email, enrollment_date)` | Create | Inserts a row and prints the new auto-generated `student_id`. Rejects duplicate emails and missing required fields. |
| `updateStudentEmail(student_id, new_email)` | Update | Changes one student's email. Reports if the ID doesn't exist or the email is already taken. |
| `deleteStudent(student_id)` | Delete | Removes the student. Reports if the ID doesn't exist. |

All queries use parameter placeholders (`%s`) to prevent SQL injection.
Each function opens its own connection, and the transaction commits automatically
when the `with` block ends successfully (or rolls back on error).
