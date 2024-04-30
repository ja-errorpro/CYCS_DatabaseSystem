import sqlite3
import pprint

def PrintTable(fetched: list):
    pprint.pprint(fetched)

database = sqlite3.connect('sample.db')
cursor = database.cursor()

# Drop table
cursor.execute("DROP TABLE IF EXISTS R")
cursor.execute("DROP TABLE IF EXISTS S")
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute("DROP TABLE IF EXISTS works")
cursor.execute("DROP TABLE IF EXISTS company")
cursor.execute("DROP TABLE IF EXISTS manages")

# Create table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS R (
        A TEXT,
        B TEXT,
        C TEXT
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS S (
        D TEXT,
        E TEXT,
        F TEXT
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS employee (
        employee_name TEXT PRIMARY KEY,
        street TEXT,
        city TEXT
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS works (
        employee_name TEXT PRIMARY KEY,
        company_name TEXT,
        salary INTEGER
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS company (
        company_name TEXT PRIMARY KEY,
        city TEXT
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS manages (
        employee_name TEXT PRIMARY KEY,
        manager_name TEXT
    )
    '''
)

database.commit()

# Insert data
cursor.execute("INSERT INTO R VALUES ('1', '2', '3')")
cursor.execute("INSERT INTO R VALUES ('4', '17', '6')")
cursor.execute("INSERT INTO R VALUES ('7', '8', '9')")
cursor.execute("INSERT INTO R VALUES ('10', '11', '12')")
cursor.execute("INSERT INTO S VALUES ('d1', 'd2', 'd3')")
cursor.execute("INSERT INTO S VALUES ('4', 'd5', 'd6')")
cursor.execute("INSERT INTO S VALUES ('6', 'd8', 'd9')")
cursor.execute("INSERT INTO employee VALUES ('Alice', 'a st', 'a city')")
cursor.execute("INSERT INTO employee VALUES ('Bob', 'b st', 'a city')")
cursor.execute("INSERT INTO employee VALUES ('Charlie', 'c st', 'b city')")
cursor.execute("INSERT INTO employee VALUES ('David', 'b st', 'a city')")
cursor.execute("INSERT INTO employee VALUES ('Floyd', 'c st', 'c city')")
cursor.execute("INSERT INTO employee VALUES ('George', 'a st', 'c city')")
cursor.execute("INSERT INTO employee VALUES ('Henry', 'c st', 'b city')")
cursor.execute("INSERT INTO employee VALUES ('Jack', 'a st', 'b city')")
cursor.execute("INSERT INTO works VALUES ('Alice', 'First Bank', 100000)")
cursor.execute("INSERT INTO works VALUES ('Bob', 'Second Bank', 200000)")
cursor.execute("INSERT INTO works VALUES ('Charlie', 'First Bank', 300000)")
cursor.execute("INSERT INTO works VALUES ('David', 'Second Bank', 400000)")
cursor.execute("INSERT INTO works VALUES ('Floyd', 'Third Bank', 500000)")
cursor.execute("INSERT INTO works VALUES ('George', 'First Bank', 500)")
cursor.execute("INSERT INTO works VALUES ('Henry', 'First Bank', 10000)")
cursor.execute("INSERT INTO works VALUES ('Ivan', 'Second Bank', 20000)")
cursor.execute("INSERT INTO company VALUES ('First Bank', 'a city')")
cursor.execute("INSERT INTO company VALUES ('Second Bank', 'b city')")
cursor.execute("INSERT INTO company VALUES ('Third Bank', 'c city')")
cursor.execute("INSERT INTO manages VALUES ('Alice', 'Charlie')")
cursor.execute("INSERT INTO manages VALUES ('Charlie', 'David')")
cursor.execute("INSERT INTO manages VALUES ('George', 'Charlie')")
cursor.execute("INSERT INTO manages VALUES ('Henry', 'Charlie')")

database.commit()

# Q1. self-join to get direct and indirect supervisors of a person (person, direct, indirect)

print('\033[1;32mQ1. self-join to get direct and indirect supervisors of a person (person, direct, indirect)\033[0m\n')

cursor.execute(
    '''
    SELECT employee.employee_name, manages.manager_name, manage_2.manager_name
    FROM employee, manages, manages as manage_2
    WHERE employee.employee_name = manages.employee_name
        AND manages.manager_name = manage_2.employee_name
    '''
)

PrintTable(cursor.fetchall())

# Q2. full outer join on two or more tables

print('\n\033[1;32mQ2. full outer join on two or more tables\033[0m\n')

cursor.execute(
    '''
    SELECT employee.*, works.*
    FROM employee
        LEFT JOIN works 
            ON employee.employee_name = works.employee_name
    UNION
    SELECT employee.*, works.*
        FROM works
            LEFT JOIN employee 
                ON employee.employee_name = works.employee_name
    '''
)

PrintTable(cursor.fetchall())

# 4-1.a Project_A (R)

print('\n\033[1;32m4-1.a Project_A (R)\033[0m\n')

cursor.execute(
    '''
    SELECT A 
    FROM R
    '''
)

PrintTable(cursor.fetchall())

# 4-1.b Project_A (σB=5(R))

print('\n\033[1;32m4-1.b Project_A ( select_{B=17}(R))\033[0m\n')

cursor.execute(
    '''
    SELECT A 
    FROM R 
    WHERE B = '17'
    '''
)

PrintTable(cursor.fetchall())

# 4-1.c R * S

print('\n\033[1;32m4-1.c R * S\033[0m\n')

cursor.execute(
    '''
    SELECT * 
    FROM R, S
    '''
)

PrintTable(cursor.fetchall())

# 4-1.d Project_A, F (σC=D(R) * S

print('\n\033[1;32m4-1.d Project_A, F ( select_{C=D}(R * S)\033[0m\n')

cursor.execute(
    '''
    SELECT A, F 
    FROM R, S 
    WHERE C = D
    '''
)

PrintTable(cursor.fetchall())

# 4-2.a find the names of all employees who work for First Bank Corporation

print('\n\033[1;32m4-2.a find the names of all employees who work for First Bank Corporation\033[0m\n')

cursor.execute(
    '''
    SELECT employee_name 
    FROM works 
    WHERE company_name = 'First Bank'
    '''
)

PrintTable(cursor.fetchall())

''' 
4-2.b find the names and cities of residence of all employees 
who work for First Bank Corporation
'''
print('''\n\033[1;32m4-2.b find the names and cities of residence of all employees 
      who work for First Bank Corporation\033[0m\n''')

cursor.execute(
    '''
    SELECT employee.employee_name, employee.city 
    FROM works, employee 
    WHERE works.company_name = 'First Bank' 
        AND works.employee_name = employee.employee_name
    '''
)

PrintTable(cursor.fetchall())

'''
4-2.c find the names, street addresses, 
and cities of residence of all employees 
who work for First Bank and earn more than $10,000
'''

print('''\n\033[1;32m4-2.c find the names, street addresses, and cities of residence of all employees 
      who work for First Bank and earn more than $10,000\033[0m\n
      ''')

cursor.execute(
    '''
    SELECT employee.employee_name, employee.street, employee.city 
    FROM works, employee 
    WHERE works.company_name = 'First Bank' 
        AND works.employee_name = employee.employee_name 
        AND works.salary > 10000
    '''
)

PrintTable(cursor.fetchall())

'''
4-3.a find all employees in the database who do not work for First Bank.
'''

print('''\n\033[1;32m4-3.a find all employees in the database who do not work for First Bank.\033[0m\n''')

cursor.execute(
    '''
    SELECT employee.employee_name
    FROM employee, works
    WHERE company_name != 'First Bank' 
        AND employee.employee_name = works.employee_name
    '''
)

PrintTable(cursor.fetchall())

'''
4-3.b find all employees in the database who live in the same cities as the companies for which they work.
'''

print('''\n\033[1;32m4-3.b find all employees in the database 
      who live in the same cities as the companies for which they work.\033[0m\n''')

cursor.execute(
    '''
    SELECT employee.employee_name
    FROM employee, works, company
    WHERE employee.city = company.city 
        AND works.company_name = company.company_name
        AND employee.employee_name = works.employee_name
    '''
)

PrintTable(cursor.fetchall())

'''
4-3.c find all employees in the database
    who live in the same cities and on the same streets as do their managers.
'''

print('''\n\033[1;32m4-3.c find all employees in the database
    who live in the same cities and on the same streets as do their managers.\033[0m\n''')

cursor.execute(
    '''
    SELECT employee.employee_name
    FROM employee, manages, employee as manager
    WHERE employee.city = manager.city 
        AND employee.street = manager.street
        AND employee.employee_name = manages.employee_name
        AND manages.manager_name = manager.employee_name
    '''
)

PrintTable(cursor.fetchall())