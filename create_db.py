import sqlite3

# Connecting to the database.
conn = sqlite3.connect("company.db") # Connecting to the database file.
cursor = conn.cursor() # Creating a cursor to execute queries.
cursor.execute("PRAGMA foreign_keys = ON;")  # Enabling foreign keys for ON DELETE CASCADE to work correctly.

def create_tables_from_dict(cursor: sqlite3.Cursor, tables_dict: dict[str, str]) -> None:
    """
    Executing SQL commands - creating tables via Python.

    Args:
        param cursor: Active database cursor used to execute SQL scripts.
        param tables_dict: Dictionary where keys are table names and values are column definitions in SQL syntax.

    Returns:
        None.
    """

    script = ""
    for table_name, table_parameters in tables_dict.items():
        script += f"CREATE TABLE IF NOT EXISTS {table_name} ({table_parameters});\n"
    cursor.executescript(script)

# Tables being created.
tables = {
    "Employees": """
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        phone_number TEXT,
        hire_date TEXT,
        job_title TEXT,
        salary REAL
    """,
    "Projects": """
        project_id INTEGER PRIMARY KEY,
        project_name TEXT,
        start_date TEXT,
        end_date TEXT,
        budget REAL
    """,
    "Project_Assignments": """
        assignment_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        project_id INTEGER,
        role TEXT,
        hours_worked INTEGER,
        FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
    """
}

create_tables_from_dict(cursor, tables)

conn.commit() # Committing changes to the database.

# # Recreate the table to add ON DELETE CASCADE to foreign keys.
# def rename_table(cursor: sqlite3.Cursor, old_name: str, new_name: str) -> None:
#     """
#     Renaming an existing table.
#
#     Args:
#         param cursor: Active database cursor used to execute SQL scripts.
#         param old_name: The name of the existing table that is being renamed.
#         param new_name: New table name.
#
#     Returns:
#         None.
#     """
#     cursor.execute(f'ALTER TABLE "{old_name}" RENAME TO "{new_name}";')
#
# rename_table(cursor, "Project_Assignments", "ProjectAssignments_old")
# conn.commit() # Committing changes to the database.
#
# def create_project_assignments_with_cascade(cursor: sqlite3.Cursor) -> None:
#     """
#     New table with cascading deletion.
#
#     Args:
#         param cursor: Active database cursor used to execute SQL scripts.
#         param cursor: Active database cursor used to execute SQL scripts.
#
#     Returns:
#         None.
#     """
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Project_Assignments(
#             assignment_id INTEGER PRIMARY KEY,
#             employee_id INTEGER,
#             project_id INTEGER,
#             role TEXT,
#             hours_worked INTEGER,
#             FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
#             FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE
#         );
#     """)
#
# create_project_assignments_with_cascade(cursor)
# conn.commit() # Committing changes to the database.
#
# def copy_data_table(cursor: sqlite3.Cursor) -> None:
#     """
#     Copying data from the old table to the new one.
#
#     Args:
#         param cursor: Active database cursor used to execute SQL scripts.
#
#     Returns:
#         None.
#     """
#
#     cursor.execute("""
#         INSERT INTO Project_Assignments(assignment_id, employee_id, project_id, role, hours_worked)
#         SELECT assignment_id, employee_id, project_id, role, hours_worked
#         FROM ProjectAssignments_old;
#     """)
#
# copy_data_table(cursor)
# conn.commit() # Committing changes to the database.
#
# def delete_table(cursor: sqlite3.Cursor, table_name: str) -> None:
#     """
#     Deleting the old table.
#
#     Args:
#         param cursor: Active database cursor used to execute SQL scripts.
#         param table_name: Deleting the old table.
#
#     Returns:
#         None.
#     """
#     if not table_name.isidentifier():
#         raise ValueError("Invalid table name.")
#     cursor.execute(f'DROP TABLE "{table_name}";')
#
# delete_table(cursor, "ProjectAssignments_old")
# conn.commit() # Committing changes to the database.

conn.close() # Closing the connection.