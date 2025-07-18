from faker import Faker
import random
from random import choice
from random import randint
from random import uniform
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Any, Tuple
import sqlite3


fake = Faker('en_GB')

# Employees table. PRIMARY_KEY = employee_id.
employees_id = list(range(1, 51))
first_names = [fake.first_name() for _ in range(50)]
last_names = [fake.last_name() for _ in range(50)]
emails = [fake.unique.email() for _ in range(50)]
phone_numbers = ['+44 ' + fake.msisdn()[3:] for _ in range(50)]
hire_dates = [fake.date_between(start_date='-5y', end_date='today').strftime('%d.%m.%Y') for _ in range(50)]

job_salary_ranges = {
    'Software Engineer': (2000, 3200),
    'Data Analyst': (2000, 3200),
    'HR Manager': (1500, 2750),
    'Project Manager': (3000, 3800),
    'QA': (1800, 2900)
}

def generate_employees(employees_id: List[int], job_salary_ranges: dict[str, tuple]) -> dict[int, dict[str, Any]]:
    """
    Generation of data for Employees table.

    Args:
        employees_id: Employee identifiers.
        job_salary_ranges: Salary ranges by position.

    Returns:
        Generated data for the Employees table.
    """
    employees = {}

    for employee_id, _ in enumerate(employees_id, start=1):
        job_title = choice(list(job_salary_ranges.keys()))
        salary = round(uniform(*job_salary_ranges[job_title]), 2)

        employees[employee_id] = {
            "employee_id": employee_id,
            "first_name": first_names[employee_id - 1],
            "last_name": last_names[employee_id - 1],
            "email": emails[employee_id - 1],
            "phone_number": phone_numbers[employee_id - 1],
            "hire_date": hire_dates[employee_id - 1],
            "job_title": job_title,
            "salary": salary
        }

    return employees

# Projects table. PRIMARY_KEY = project_id.
projects_id = list(range(1, 11))

projects_name = [fake.bs().title() for _ in range(10)]

project_dates_budget = {}

for project_name in projects_name:
    start_date = fake.date_between(start_date=(datetime.today() - timedelta(days=548)), end_date='today')
    end_date = fake.date_between(start_date=start_date, end_date=(datetime.today() + timedelta(days=150)))
    project_dates_budget[project_name] = {
        'start_date': start_date.strftime('%d.%m.%Y'),
        'end_date': end_date.strftime('%d.%m.%Y'),
        'budget': f"{round(uniform(5000, 10000), 2)}£"
    }

def generate_projects(projects_id: List[int], projects_name: List[str]) -> dict[int, dict[str, Any]]:
    """
    Generation of data for Projects table.

    Args:
        projects_id: Projects identifiers.
        projects_name: Created names for projects.

    Returns:
        Generated data for the Projects table.
    """
    projects = {}

    for project_id, _ in enumerate(projects_id, start=1):
        project_name = projects_name[project_id - 1]
        projects[project_id] = {
            "project_id": project_id,
            "project_name": project_name,
            "start_date": project_dates_budget[project_name]['start_date'],
            "end_date": project_dates_budget[project_name]['end_date'],
            "budget": project_dates_budget[project_name]['budget'],
        }

    return projects

# Project_Assignments Table. PRIMARY_KEY = assignment_id.
main_roles = [ 'Software Engineer','Project Manager', 'QA']

def generate_project_assignments(employees_id: List[int], projects_id: List[int], main_roles: List[str], employees: dict[int, dict[str, Any]]) -> dict[int, dict[str, int]]:
    """
    Generation of data for Project_Assignments table.

    Args:
        employees_id: Employee identifiers.
        projects_id: Projects identifiers.
        main_roles: Mandatory positions in the project.
        employees: Generated employees data used to assign roles.

    Returns:
        Data for the Projects table.
    """
    # Preparation of storage.
    employee_projects = defaultdict(set)  # Each employee's projects.
    project_employees = defaultdict(set)  # Employees on each project.

    # Assigning 1–3 projects to each employee
    for employee_id in employees_id:
        number_projects = random.randint(1, 3)
        selected_projects = random.sample(projects_id, k=number_projects)

        for project_id in selected_projects:
            # Skip if the employee is already working on 3 projects.
            if len(employee_projects[employee_id]) >= 3:
                break

            # Skip if there are already 10 people in the project or the employee is already there.
            if len(project_employees[project_id]) >= 10 or project_id in employee_projects[employee_id]:
                continue

            # If there are fewer than three people in the project and the role is not a primary one, we skip it.
            if len(project_employees[project_id]) < 3 and employees[employee_id]['job_title'] not in main_roles:
                continue

            # Add connection.
            employee_projects[employee_id].add(project_id)
            project_employees[project_id].add(employee_id)

    # Forced assignment of a project if no project could be assigned.
    for employee_id in employees_id:
        while len(employee_projects[employee_id]) < 1:
            project_id = random.choice(projects_id)
            if (len(project_employees[project_id]) < 10 and project_id not in employee_projects[employee_id]):
                employee_projects[employee_id].add(project_id)
                project_employees[project_id].add(employee_id)

    # Confirmation that each project has at least 3 employees and no employee is assigned to more than 3 projects.
    for project_id in projects_id:
        while len(project_employees[project_id]) < 3:
            possible_employee = random.choice(employees_id)

            # Check that this employee has fewer than 3 projects.
            if len(employee_projects[possible_employee]) < 3:
                employee_projects[possible_employee].add(project_id)
                project_employees[project_id].add(possible_employee)

    # ProjectAssignments Table. PRIMARY_KEY = assignment_id. FOREIGN KEYs = employee_id (Employees), project_id (Projects)
    project_assignments = {}

    assignment_id = 1

    for employee_id, project_ids in employee_projects.items():
        for project_id in project_ids:
            hours = randint(10, 120)
            project_assignments[assignment_id] = {
                "assignment_id": assignment_id,
                "employee_id": employee_id,
                "project_id": project_id,
                "role": employees[employee_id]['job_title'],
                'hours_worked': hours
            }
            assignment_id += 1

    return project_assignments

def get_generated_data() -> Tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], dict[int, dict[str, int]]]:
    """
    Generates full dataset for Employees, Projects, and Project Assignments.

    Returns:
        Tuple containing:
            - employees: Employee records.
            - projects: Project records.
            - project_assignments: Employee-project assignment records.
    """
    employees = generate_employees(employees_id, job_salary_ranges)
    projects = generate_projects(projects_id, projects_name)
    project_assignments = generate_project_assignments(employees_id, projects_id, main_roles, employees)
    return employees, projects, project_assignments

if __name__ == "__main__":
    employees, projects, project_assignments = get_generated_data()
    print("employees:", employees)
    print("projects:", projects)
    print("project_assignments:", project_assignments)

with sqlite3.connect("company.db") as conn:
    cursor = conn.cursor()

def columns_names_list(table_data: dict[int, dict[str, Any]]) -> List[str]:
    """
    Extract a list of column names from generated table data.

    Args:
        table_data: A dictionary containing rows of a table, where keys are row IDs and values are dictionaries representing each row.

    Returns:
        A sorted list of column names for the table.
    """
    return sorted(list(next(iter(table_data.values())).keys()))

employees_columns_names = columns_names_list(employees)
projects_columns_names = columns_names_list(projects)
project_assignments_columns_names = columns_names_list(project_assignments)

def columns_str(columns_names_list: List[str]) -> str:
    """
    Convert a list of column names into a comma-separated string.

    Args:
        columns_names_list: A list of column names.

    Returns:
        A string suitable for use in SQL queries.
    """
    return ', '.join(columns_names_list)

employees_columns_str = columns_str(employees_columns_names)
projects_columns_str = columns_str(projects_columns_names)
project_assignments_columns_str = columns_str(project_assignments_columns_names)

def placeholders(columns_names_list: List[str]) -> str:
    """
    Generate a comma-separated string of SQL placeholders based on the number of columns.

    Args:
        columns_names_list: A list of column names.

    Returns:
        A string of placeholders (e.g., '?, ?, ?') for use in SQL INSERT statements.
    """
    return ', '.join(['?'] * len(columns_names_list))

employees_placeholders = placeholders(employees_columns_names)
projects_placeholders = placeholders(projects_columns_names)
project_assignments_placeholders = placeholders(project_assignments_columns_names)

def insert_data(table_name: dict[int, dict[str, Any]], columns_names: List[str], columns_str: str, placeholders: str, table_sql_name: str) -> None:
    """
    Insert data into an SQLite table.

    Args:
        table_data: A dictionary containing the table's data, where each value is a dictionary representing a row.
        columns_names: A list of column names.
        columns_str: A comma-separated string of column names for the SQL query.
        placeholders: A comma-separated string of SQL placeholders (e.g., '?, ?, ?').
        table_sql_name: The name of the target table in the database.

    Returns:
        None.
    """
    try:
        for row in table_name.values():
            values_tuple = tuple(row[column] for column in columns_names)
            cursor.execute(f'''
                INSERT OR IGNORE INTO {table_sql_name} ({columns_str})
                VALUES ({placeholders})
            ''', values_tuple)

        conn.commit()
        print(f"Data successfully inserted into table '{table_sql_name}'.")

    except sqlite3.IntegrityError as e:
        print(f"Error when inserting data into {table_sql_name}:", e)

insert_data(employees, employees_columns_names, employees_columns_str, employees_placeholders, "Employees")
insert_data(projects, projects_columns_names, projects_columns_str, projects_placeholders, "Projects")
insert_data(project_assignments, project_assignments_columns_names, project_assignments_columns_str, project_assignments_placeholders, "Project_Assignments")




