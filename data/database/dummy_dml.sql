INSERT INTO company(_name)
VALUES
    ('Company 1'),
    ('Company 2'),
    ('Company 3')
;

INSERT INTO division (_name, location, accounts_payable_name, accounts_payable_email)
VALUES ('Division 1', 'Location 1', 'Name 1', 'email1@example.com'),
       ('Division 2', 'Location 2', 'Name 2', 'email2@example.com'),
       ('Division 3', 'Location 3', 'Name 3', 'email3@example.com')
;

INSERT INTO company_division (company_id, division_id)
VALUES (1, 1),
       (1, 2),
       (1, 3)
;

INSERT INTO project (_name, address, company_id, division_id)
VALUES ('project 1', 'Address 1', 1, 1),
       ('project 2', 'Address 2', 1, 2),
       ('project 3', 'Address 3', 2, 2),
       ('project 4', 'Address 4', 3, 2),
       ('project 5', 'Address 5', 1, 3)
;

INSERT INTO employee (_name, phone_number, email)
VALUES ('Name 1', 'Phone 1', 'Email 1'),
       ('Name 2', 'Phone 2', 'Email 2'),
       ('Name 3', 'Phone 3', 'Email 3')
;

INSERT INTO supervisor  (_name, phone_number, email)
VALUES ('Name 1', 'Phone 1', 'Email 1'),
       ('Name 2', 'Phone 2', 'Email 2'),
       ('Name 3', 'Phone 3', 'Email 3')
;

INSERT INTO order_status (_status)
VALUES  ('PAID'),
        ('SHORT-PAID'),
        ('APPROVED'),
        ('PRE-APPROVED'),
        ('SENT'),
        ('NOT-PAID'),
        ('REVIEWING'),
        ('NOT-SENT'),
        ('VOID')
;

INSERT INTO order_type (_type)
VALUES  ('EWO'),
        ('WARR'),
        ('CONTRACT')
;

INSERT INTO _order (_type_id, _status_id, project_id, order_number, unit_address, full_address,
                    supervisor_id, employee_id, _date, amount, note)
VALUES (1, 3, 3, '2444', '5/4', '10001 SW 1st Ave',1, 1, '2023-01-01', 10000, 'note#1'),
       (1, 3, 2, '2445', '6/4', '10002 SW 2st Ave',2, 2, '2023-02-02', 10001, 'note#2'),
       (2, 3, 2, '2446', '7/4', '10003 SW 3st Ave',3, 3, '2023-02-03', 10002, 'note#3'),
       (3, 3, 2, '2447', '8/4', '10004 SW 4st Ave',1, 2, '2023-03-01', 10003, 'note#4'),
       (1, 3, 2, '2448', '9/4', '10005 SW 5st Ave',3, 1, '2023-04-25', 10004, 'note#5')
;

INSERT INTO preferred_project_employee (project_id, employee_id)
VALUES (1,1),
       (2,2),
       (3,3)
;