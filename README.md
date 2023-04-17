# Supplier-Order-Management-Software
Supplier Order Management Software (SOMS) was designed to insert, modify, delete, import, and email orders from a supplier to its business partners. Generates email drafts by finding, and sorting orders and their attachments to resolve issues with the collection of payments. The email generation is based on orders saved on a database.

# Dependencies
*Please use `pip install -r requirements.txt` to install all the dependencies*  
It is possible to have it working with more recent versions of each dependency but to prevent issues please use the versions mentioned. For your convenience they are also listed here:  
  
From *requirements.txt*:
```
Babel==2.12.1
pywin32==306
tkcalendar==1.6.1
```

### Database Diagram
The database uses foreign keys and intersection tables to relate the tables. Please note that the primary keys are in yellow while the foreign keys are in blue.
![Database Relational Diagram](https://user-images.githubusercontent.com/11873738/232396864-d99b8a48-12c6-4991-ab57-0ae8f62d6bb6.png)
