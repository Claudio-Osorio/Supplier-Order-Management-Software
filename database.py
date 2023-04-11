import os
import sqlite3
from configurations import *
from exceptions import *
import shutil
import time
import logging

def validate_database():
    logging.info("Database: Validating database")
    db_path = os.path.abspath(os.getcwd() + read_database_path())
    if not check_database_exists(db_path):
        logging.warning("Database: Database file not found. "
                        "A new default database will be initialized")
        create_init_database(db_path)
        logging.info("Database: New Database created. "
                     "DDL execution complete")
        # if read_debug_mode():
        #     insert_dummy_data_dml(db_path)
        # else:
        #     insert_restore_data_dml(db_path)
        insert_restore_data_dml(db_path)

        logging.info("Database: New Database default values added. "
                     "DML execution complete")

def check_database_exists(db_path):
    return os.path.exists(db_path)

def create_init_database(db_path):
    execute_script_on_db(db_path, read_DDL_path())

def insert_restore_data_dml(db_path):
    execute_script_on_db(db_path, read_restored_DML_path())

def insert_dummy_data_dml(db_path):
    execute_script_on_db(db_path, read_dummy_DML_path())

def execute_script_on_db(db_path, script_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if not os.path.exists(os.path.abspath(os.getcwd()) + script_path):
        raise Exception(f"""Database script file @{script_path} not found. Program will exit.""")
    script = open(os.path.abspath(os.getcwd()) + script_path, "r")
    try:
        c.executescript(script.read())
        logging.info("Database: Successfully executed script \"" + str(script_path) + "\"")
    except:
        raise Exception(f"""Database script file @{script_path} could not be read. Program will exit.""")
    finally:
        script.close()

def create_connection():
    try:
        conn = sqlite3.connect(os.path.abspath(os.getcwd() + read_database_path()))
    except Exception:
        raise DatabaseConnectionError("Database connection failed.")
    return conn

# Creates a transaction, returns connection and cursor
def create_transaction():
    conn = create_connection()
    c = conn.cursor()
    sql = "BEGIN TRANSACTION"
    c.execute(sql)
    return conn, c

def execute_query(sql,*value):
    conn = create_connection()
    c = conn.cursor()
    start_time = time.perf_counter()
    if value:
        c.execute(sql, value)
    else:
        c.execute(sql)
    tables = c.fetchall()
    end_time = time.perf_counter()
    conn.close()
    elapsed_time_ms = (end_time - start_time) * 1000
    logging.info(f"Database: Query request elapsed time: {elapsed_time_ms:.2f} ms")
    return tables

def get_name_of_all_employees():
    sql = f"""
    SELECT id, _name 
    FROM employee
    ORDER BY _name
    """
    return execute_query(sql)

# Returns list of tuples
def get_name_of_all_supervisors():
    sql = f"""
    SELECT id, _name FROM supervisor
    ORDER BY _name
    """
    return execute_query(sql)

# Returns list of tuples
def get_name_of_all_companies():
    sql = f"""
    SELECT id, _name FROM company
    ORDER BY _name
    ;
    """
    return execute_query(sql)

# Returns list of tuples
def get_all_projects(company_id):
    sql = f"""
    SELECT id, _name FROM project
    WHERE company_id = ?
    ORDER BY _name
    """
    return execute_query(sql, company_id)

def get_order_by_id(_id):
    sql = f"""
    SELECT * FROM _order
    WHERE id = ?
    """
    return execute_query(sql, _id)

def get_all_order_status():
    sql = f"""
    SELECT id, _status FROM order_status
    """
    return execute_query(sql)

def get_all_types():
    sql = f"""
    SELECT id, _type FROM order_type
    """
    return execute_query(sql)

def get_preferred_employee(project_id):
    sql = f"""
    SELECT employee_id FROM preferred_project_employee
    WHERE project_id = ?"""
    return execute_query(sql,project_id)

def store_new_order(data):
    conn, c = create_transaction()
    sql = """
    INSERT INTO _order(_date,
                    supervisor_id,
                    employee_id,
                    _status_id,
                    project_id,
                    order_number,
                    unit_address,
                    full_address,
                    _type_id,
                    amount,
                    note,
                    external_tracking)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (data["_order._date"],
            data["_order.supervisor_id"],
            data["_order.employee_id"],
            data["_order.status"],
            data["_order.project_id"],
            data["_order.order_number"],
            data["_order.unit_address"],
            data["_order.full_address"],
            data["_order._type"],
            data["_order.amount"],
            data["_order.note"],
            data["_order.external_tracking"])
    c.execute(sql,values)
    new_order_id = c.lastrowid
    conn.commit()
    logging.info(f"""Database: New order inserted - """
                 f"""New Order Id:{new_order_id}""")

    src = data['attachment_path']
    filename = str(new_order_id) + '-' + \
               str(data['_order.order_number']) + \
               '.pdf'
    dst = os.getcwd() + \
          read_attachment_partial_path() + \
          filename
    copied = shutil.copy2(src, dst)
    if copied:
        sql = """
        UPDATE _order
        SET attachment_name = ?
        WHERE id = ?
        """
        values = (filename, new_order_id)
        c.execute(sql,values)
        conn.commit()
    conn.close()

def store_new_supervisor(data):
    conn, c = create_transaction()
    sql = """INSERT INTO supervisor (_name, phone_number, email)
     VALUES (?, ?, ?)"""
    values = (data["name"],
              data["phone"],
              data["email"])
    c.execute(sql, values)
    conn.commit()
    conn.close()
    logging.info(f"""Database: New supervisor inserted - """
                 f"""{data["name"]}""")

def store_new_employee(data):
    conn, c = create_transaction()
    sql = """INSERT INTO employee (_name, phone_number, email)
     VALUES (?, ?, ?)"""
    values = (data["name"],
              data["phone"],
              data["email"])
    c.execute(sql, values)
    new_employee_id = c.lastrowid
    conn.commit()
    conn.close()
    logging.info(f"""Database: New employee inserted - """
                 f"""{data["name"]}""")
    return new_employee_id

def store_new_company(data):
    conn, c = create_transaction()
    sql = """INSERT INTO company (_name)
    VALUES(?)
    """
    values = (data["_name"],)
    c.execute(sql, values)
    new_company_id = c.lastrowid
    conn.commit()
    conn.close()
    logging.info(f"""Database: New company inserted - """
                 f"""{data["_name"]}""")
    return new_company_id

def store_new_division(company_id, data):
    conn, c = create_transaction()
    sql = """INSERT INTO division (_name, location,
     accounts_payable_name, accounts_payable_email)
     VALUES (?,?,?,?)"""

    values = (data["division._name"],
              data["division.location"],
              data["division.accounts_payable_name"],
              data["division.accounts_payable_email"])
    c.execute(sql, values)
    logging.info(f"""Database: New division inserted - """
                 f"""{data["division._name"]}""")
    new_division_id = c.lastrowid

    sql = """INSERT INTO company_division (company_id,
     division_id)
     VALUES (?,?)"""
    values = (company_id, new_division_id)
    c.execute(sql, values)
    conn.commit()
    conn.close()
    logging.info(f"Database: New company, division inserted -"
                 f" {company_id}, {new_division_id}")
    return new_division_id

def store_new_project(data):
    conn, c = create_transaction()
    sql = """INSERT INTO project (_name, address, company_id, division_id)
    VALUES(?,?,?,?)
    """
    values = (data["project._name"],
              data["project.address"],
              data["project.company_id"],
              data["project.division_id"])
    c.execute(sql, values)
    new_project_id = c.lastrowid
    conn.commit()
    logging.info(f"Database: New project inserted - {values[0]}")
    sql = """INSERT INTO preferred_project_employee(project_id, employee_id)
    VALUES(?,?)
    """
    values = (new_project_id, data["employee.id"])
    c.execute(sql, values)
    conn.commit()
    logging.info(f"Database: New preferred project-employee"
                 f" inserted - {values[0]},{values[1]}")
    conn.close()
    return new_project_id

def store_new_preferred_employee(employee_id, list_projects):
    conn, c = create_transaction()
    for project_id in list_projects:
        sql = """INSERT INTO preferred_project_employee (project_id, employee_id)
        VALUES(?,?)
        """
        values = (project_id, employee_id)
        c.execute(sql, values)
        logging.info(f"Database: New preferred project-employee inserted"
                     f" - {project_id},{employee_id}")
    conn.commit()
    conn.close()

def get_all_divisions(company_id):
    sql = """SELECT division.id, division._name
     FROM company_division
     INNER JOIN division
     ON company_division.division_id = division.id
     WHERE company_division.company_id = ?"""

    return execute_query(sql, company_id)

def delete_order(order_id):
    conn, c = create_transaction()
    sql = """DELETE FROM _order
     WHERE id = ?"""
    c.execute(sql, (order_id,))
    conn.commit()
    conn.close()
    logging.info(f"Database: Order Id:{order_id} - Successfully deleted")

def delete_preferred_employee(list_projects):
    conn = create_connection()
    c = conn.cursor()
    for project_id in list_projects:
        sql = """DELETE FROM preferred_project_employee
        WHERE project_id = ?"""
        c.execute(sql, (project_id,))
        logging.info(f"Database: Project Id:{project_id} preferred employee has been deleted")
    conn.commit()
    conn.close()
