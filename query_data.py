import sqlite3
import csv
from typing import List, Any, Optional, Tuple

# Connecting to the database.
with sqlite3.connect("company.db") as conn:
    cursor = conn.cursor()

def query_data(cursor: sqlite3.Cursor, request: str, params: tuple = ()) -> List[Any]:
    """
    Executes a SQL query that returns multiple rows.

    Args:
        cursor: Active database cursor.
        request: SQL query string.
        params: Tuple of parameters for the SQL query.

    Returns:
        A list of tuples with the query result rows.
    """
    try:
        cursor.execute(request, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def query_one_data(cursor: sqlite3.Cursor, request: str, params: tuple = ()) -> Optional[Any]:
    """
    Executes a SQL query that returns a single value.

    Args:
        cursor: Active database cursor.
        request: SQL query string.
        params: Tuple of parameters for the query.

    Returns:
        A single value or None.
    """
    try:
        cursor.execute(request, params)
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def screen_result(data: List[tuple], columns: List[str]) -> None:
    """
    Displays the query result in a tabular format.

    Args:
        data: List of tuples with data rows.
        columns: List of column headers.

    Returns:
        None.
    """
    if not data:
        print("No data found.")
        return

    col_widths = [] # Calculating the width of each column.
    for i in range(len(columns)):
        max_data_width = max(len(str(row[i])) for row in data)
        col_width = max(len(columns[i]), max_data_width)
        col_widths.append(col_width + 2)

    # Print header.
    header = '| ' + ' | '.join(f"{columns[i]:<{col_widths[i]}}" for i in range(len(columns))) + ' |'
    print('-' * len(header))
    print(header)
    print('-' * len(header))

    # Print a string of data.
    for row in data:
        row_str = '| ' + ' | '.join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(columns))) + ' |'
        print(row_str)
    print('-' * len(header))

# List of all employees (first_name, last_name, email, job_title), sorted by last name.
all_employees_request = """
    SELECT first_name, last_name, email, job_title
    FROM Employees
    ORDER BY last_name
"""

all_employees = query_data(cursor, all_employees_request) # Getting all the result rows.
employees_columns = ['first_name', 'last_name', 'email', 'job_title']
screen_result(all_employees, employees_columns)

# Project details (project_name, start_date, end_date, budget) for all projects.
projects_details_request = """
    SELECT project_name, start_date, end_date, budget
    FROM Projects
"""

projects_details = query_data(cursor, projects_details_request) # Getting all the result rows.
projects_columns = ['project_name', 'start_date', 'end_date','budget']
screen_result(projects_details, projects_columns)

# List of employees assigned to the project (first_name, last_name, role, hours_worked) upon user request.
project_name = input("Enter the project name: ") # User request.

project_id_request = """
    SELECT project_id
    FROM Projects
    WHERE project_name = ?
"""

project_id = query_one_data(cursor, project_id_request, (project_name,)) # Obtaining a single line of results.

employees_in_project_request = """
    SELECT e.first_name, e.last_name, pa.role, pa.hours_worked
    FROM Employees e
    INNER JOIN Project_Assignments pa ON e.employee_id = pa.employee_id
    WHERE pa.project_id = ?
"""
employees_in_project = query_data(cursor, employees_in_project_request, (project_id,))

employees_in_project_columns = ['first_name', 'last_name', 'role', 'hours_worked']
screen_result(employees_in_project, employees_in_project_columns)

# List of all projects (project_name, role, hours_worked) by email on user request.
email = input("Enter the email: ")

employee_id_request = """
    SELECT employee_id
    FROM Employees
        WHERE email = ?
"""
employee_id = query_one_data(cursor, employee_id_request, (email,)) # Obtaining a single line of results.

projects_in_employee_request = """
    SELECT p.project_name, pa.role, pa.hours_worked
    FROM Project_Assignments pa
    INNER JOIN Employees e ON pa.employee_id = e.employee_id
    INNER JOIN Projects p ON pa.project_id = p.project_id
    WHERE e.employee_id = ?
"""
projects_in_employee = query_data(cursor, projects_in_employee_request, (employee_id,))
projects_in_employee_columns = ['project_name', 'role', 'hours_worked']
screen_result(projects_in_employee, projects_in_employee_columns)

# Top 3 highest paid employees (first_name, last_name, salary).
three_max_salary_request = """
    SELECT first_name, last_name, salary
    FROM Employees
    ORDER BY salary DESC
    LIMIT 3
"""
three_max_salary = query_data(cursor, three_max_salary_request)
three_max_salary_columns = ['first_name', 'last_name', 'salary']
screen_result(three_max_salary, three_max_salary_columns)

# Average salary by position (job_title, average salary for each position).
average_salary_position_request ="""
    SELECT job_title, AVG(salary) as average_salary
    FROM Employees
    GROUP BY job_title
"""
average_salary_position = query_data(cursor, average_salary_position_request)
average_salary_position_columns = ['job_title', 'average_salary']
screen_result(average_salary_position, average_salary_position_columns)

def query_update(employee_id: int, job_title: str, salary: int, project_id: int, end_date: str) -> None:
    """
    Updates an employee's job title and salary, and updates the end date of a project.

    Args:
        employee_id: ID of the employee to update.
        job_title: New job title to assign.
        salary: New salary value.
        project_id: ID of the project to update.
        end_date: New project end date (format: 'DD.MM.YYYY').

    Returns:
        None.
    """
    try:
        cursor.execute("""
            UPDATE Employees
            SET job_title = ?, salary = ?
            WHERE employee_id = ?
        """, (job_title,salary, employee_id))

        cursor.execute("""
            UPDATE Projects
            SET end_date = ?
            WHERE project_id = ?
        """, (end_date, project_id))

        conn.commit()
        print("Update successful.")

    except sqlite3.Error as e:
        print(f"Update failed: {e}")
        conn.rollback()

query_update(1, 'QA', 2400, 1, '06.08.2025')

def delete_employee(employee_id: int) -> None:
    """
    Deletes an employee and all related records in Project_Assignments.

    Args:
        employee_id: ID of the employee to delete.
    """
    try:
        cursor.execute("DELETE FROM Project_Assignments WHERE employee_id = ?", (employee_id,))
        cursor.execute("DELETE FROM Employees WHERE employee_id = ?", (employee_id,))
        conn.commit()
        print(f"Employee {employee_id} deleted.")
    except sqlite3.Error as e:
        print(f"Failed to delete employee: {e}")
        conn.rollback()

delete_employee(1)

def delete_project(project_id: int) -> None:
    """
    Deletes a project and all related records in Project_Assignments.

    Args:
        project_id: ID of the project to delete.
    """
    try:
        cursor.execute("DELETE FROM Project_Assignments WHERE project_id = ?", (project_id,))
        cursor.execute("DELETE FROM Projects WHERE project_id = ?", (project_id,))
        conn.commit()
        print(f"Project {project_id} deleted.")
    except sqlite3.Error as e:
        print(f"Failed to delete project: {e}")
        conn.rollback()

delete_project(2)

# Modifying query_data.py so that the results of one of the queries (e.g., "List of all employees" or "Employees in a specific
# project") can be exported to a CSV or JSON file.
def export(file_name: str, data: List[Tuple[Any, ...]], title: List[str], header: List[str]) -> None:
    """
    Exports the result data to a CSV file.

    Args:
        file_name: Output CSV file name.
        data: List of tuples with query results.
        title: List with section title (as a row).
        header: Column headers.

    Returns:
        None.
    """
    try:
        with open(file_name, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(title)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)
        print(f"Data exported to {file_name}")
    except Exception as e:
        print(f"Export failed: {e}")

title = ["LIST_OF_EMPLOYEES:"]
header = ["first_name", "last_name", "email", "job_title"]
export("all_employees.csv", all_employees, title, header)

