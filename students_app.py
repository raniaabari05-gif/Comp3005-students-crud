"""
students_app.py

A small command-line application that connects to a PostgreSQL database
and performs CRUD operations on the "students" table:

    getAllStudents()                                   -> Read
    addStudent(first_name, last_name, email, date)     -> Create
    updateStudentEmail(student_id, new_email)          -> Update
    deleteStudent(student_id)                          -> Delete

Connection settings are read from environment variables so no passwords
are hard-coded (see README.md):
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
"""

import os
import sys
from datetime import date

import psycopg2
from psycopg2 import errors


# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

# Connection parameters, with sensible defaults for a local pgAdmin install.
DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "students_db"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
}


def get_connection():
    """Open and return a new connection to the PostgreSQL database.

    Exits the program with a readable message if the database is unreachable,
    rather than showing a long stack trace.
    """
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# CRUD functions
# ---------------------------------------------------------------------------

def getAllStudents():
    """READ: retrieve every row in the students table and print it as a table."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT student_id, first_name, last_name, email, enrollment_date "
            "FROM students ORDER BY student_id;"
        )
        rows = cur.fetchall()

    # Print a simple fixed-width table so the output is easy to read in the demo.
    print(f"\n{'ID':<4} {'First':<12} {'Last':<12} {'Email':<30} {'Enrolled':<10}")
    print("-" * 72)
    for sid, first, last, email, enrolled in rows:
        print(f"{sid:<4} {first:<12} {last:<12} {email:<30} {str(enrolled or ''):<10}")
    print(f"({len(rows)} row(s))\n")
    return rows


def addStudent(first_name, last_name, email, enrollment_date):
    """CREATE: insert a new student and return the auto-generated student_id.

    A parameterized query (%s placeholders) is used so user input is never
    pasted directly into SQL, which prevents SQL injection.
    """
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id;",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
        # Leaving the "with conn" block commits the transaction.
        print(f"Added student {first_name} {last_name} with ID {new_id}.")
        return new_id
    except errors.UniqueViolation:
        # Raised when the email already exists (UNIQUE constraint).
        print(f"Error: a student with email '{email}' already exists.")
    except errors.NotNullViolation:
        print("Error: first name, last name and email are all required.")
    except (errors.InvalidDatetimeFormat, errors.DatetimeFieldOverflow):
        print("Error: enrollment date must be a valid date in YYYY-MM-DD format.")
    return None


def updateStudentEmail(student_id, new_email):
    """UPDATE: change the email of the student with the given student_id.

    Returns True if a row was updated, False otherwise.
    """
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount  # number of rows affected
        if updated:
            print(f"Updated email for student {student_id} to {new_email}.")
            return True
        print(f"No student found with ID {student_id}.")
    except errors.UniqueViolation:
        print(f"Error: the email '{new_email}' is already used by another student.")
    except errors.NotNullViolation:
        print("Error: email cannot be empty.")
    return False


def deleteStudent(student_id):
    """DELETE: remove the student with the given student_id.

    Returns True if a row was deleted, False if no such student existed.
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        deleted = cur.rowcount
    if deleted:
        print(f"Deleted student {student_id}.")
        return True
    print(f"No student found with ID {student_id}.")
    return False


# ---------------------------------------------------------------------------
# Interactive menu (used for the demonstration video)
# ---------------------------------------------------------------------------

def read_int(prompt):
    """Keep asking until the user enters a whole number."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a valid number.")


def read_date(prompt):
    """Ask for a date in YYYY-MM-DD format; blank input means no date (NULL)."""
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Please use the format YYYY-MM-DD, or leave blank.")


def main():
    """Show a menu and call the matching CRUD function until the user quits."""
    menu = (
        "=== Students Database ===\n"
        "1. View all students\n"
        "2. Add a student\n"
        "3. Update a student's email\n"
        "4. Delete a student\n"
        "5. Exit\n"
    )
    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            enrolled = read_date("Enrollment date (YYYY-MM-DD, blank for none): ")
            # Empty strings are treated as missing so NOT NULL is enforced.
            addStudent(first or None, last or None, email or None, enrolled)
        elif choice == "3":
            sid = read_int("Student ID: ")
            new_email = input("New email: ").strip()
            updateStudentEmail(sid, new_email or None)
        elif choice == "4":
            sid = read_int("Student ID to delete: ")
            deleteStudent(sid)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-5.\n")


# Run the menu only when this file is executed directly (not when imported).
if __name__ == "__main__":
    main()
