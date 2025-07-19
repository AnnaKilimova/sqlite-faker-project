# SQLite Faker Project

A project for generating fake data using the [Faker](https://faker.readthedocs.io/) library and saving it to an SQLite database.  
Useful for practising working with databases and automatically filling tables with test data.

---

## Installation
### 1. Cloning a repository:
```bash
git clone https://github.com/AnnaKilimova/sqlite-faker-project.git
cd sqlite-faker-project
```
### 2. Creating and activating of a virtual environment:
#### For MacOS/Linux:
```bash
python3 -m venv sfp-venv
source sfp-venv/bin/activate    
```  
### For Windows:
```bash
sfp-venv\Scripts\activate    
```
### 3. Installing dependencies:
```bash
pip install -r requirements.txt    
```
## Script execution
### 1. Database creation:
```bash
python create_db.py
```
### 2. Generating and adding fake data:
```bash
python generate_data.py
```
### 3. Executing database queries:
```bash
python query_data.py
```
## File description
* create_db.py - creates an SQLite database and tables.
* generate_data.py - uses Faker to generate test data and saves it to the database.
* query_data.py - performs data sampling from the database and displays the result.
* requirements.txt - project dependency list.
* README.md - this file with the project description.
## Dependencies
- Faker — fake data generation
- sqlite3 — built-in support for SQLite (the default library in Python)
## Note
- The .gitignore file excludes::
   - Virtual environment (sfp-venv/)
   - Python caches (__pycache__/, *.pyc)
   - SQLite databases (*.db, *.sqlite3)
   - IDE settings files (.idea/)
## Licence
* This project is distributed under a free licence. Use it for educational purposes and at your discretion.