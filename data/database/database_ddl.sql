CREATE TABLE company
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
_name TEXT NOT NULL
);

CREATE TABLE division
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
_name TEXT NOT NULL,
location TEXT,
accounts_payable_name TEXT,
accounts_payable_email TEXT
);

CREATE TABLE company_division
(
company_id		INTEGER NOT NULL,
division_id		INTEGER NOT NULL,
PRIMARY KEY (company_id, division_id),
FOREIGN KEY (company_id) REFERENCES company(id),
FOREIGN KEY (division_id) REFERENCES division(id)
);

-- TODO: See if i can remove company_id   INTEGER, from this.
CREATE TABLE project
(
id				        INTEGER PRIMARY KEY AUTOINCREMENT,
_name			        TEXT NOT NULL,
address			        TEXT,
company_id		        INTEGER NOT NULL,
division_id		        INTEGER NOT NULL,
FOREIGN KEY (company_id, division_id) REFERENCES company_division(company_id, division_id)
);

CREATE TABLE employee
(
id				INTEGER PRIMARY KEY AUTOINCREMENT,
_name			TEXT NOT NULL,
phone_number	TEXT,
email			TEXT
);

CREATE TABLE supervisor
(
id				INTEGER PRIMARY KEY AUTOINCREMENT,
_name			TEXT NOT NULL,
phone_number	TEXT,
email			TEXT NOT NULL
);

CREATE TABLE order_status
(
id				INTEGER PRIMARY KEY AUTOINCREMENT,
_status			TEXT NOT NULL
);

CREATE TABLE order_type
(
id				INTEGER PRIMARY KEY AUTOINCREMENT,
_type			TEXT NOT NULL
);

CREATE TABLE _order
(
id				    INTEGER PRIMARY KEY AUTOINCREMENT,
_type_id       	    INTEGER NOT NULL,
_status_id			INTEGER NOT NULL,
project_id	        INTEGER NOT NULL,
order_number	    INTEGER NOT NULL,
unit_address	    TEXT COLLATE NOCASE,
full_address	    TEXT COLLATE NOCASE,
supervisor_id       INTEGER NOT NULL,
employee_id        INTEGER NOT NULL,
_date			    TEXT NOT NULL,
amount			    INTEGER NOT NULL,
external_tracking   TEXT COLLATE NOCASE,
note			    TEXT,
attachment_name     TEXT,
FOREIGN KEY (_status_id) REFERENCES order_status(id),
FOREIGN KEY (project_id) REFERENCES project(id),
FOREIGN KEY (_type_id) REFERENCES order_type(id)
);

CREATE TABLE preferred_project_employee
(
    project_id    INTEGER UNIQUE NOT NULL,
    employee_id    INTEGER NOT NULL,
    PRIMARY KEY (project_id, employee_id),
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);