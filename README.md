# Supplier-Order-Management-Software
Supplier Order Management Software (SOMS) was designed to insert, modify, delete, import, and email orders from a supplier to its business partners. Generates email drafts by finding, and sorting orders and their attachments to resolve issues with the collection of payments. The email generation is based on orders saved on a database.

## Dependencies
*Please use `pip install -r requirements.txt` to install all the dependencies*  
It is possible to have it working with more recent versions of each dependency but to prevent issues please use the versions mentioned. For your convenience they are also listed here:  
  
From *requirements.txt*:
```
Babel==2.12.1
pywin32==306
tkcalendar==1.6.1
```

## Functionality

### Generating Emails From Orders
Steps:
1. Select one or multiple orders
2. Press Send Selected

Result:
Emails are generated based on the pre-stored orders. The order attachments are added as attachments to the emails. Tables are generated based on the status of the orders. For each supervisor a new email is created. The tables have a header that can be customized for instructions. The "Age" of the order is calculated based on the date of the order. The orders may have a Lot and Block address or a full "regular" address. In any case when the order is created it is mandatory to have one of these fields but it is possible to have both. The email will include all of these fields if they are available. The email has a custom header, and Carbon Copy (aka CC) which can be modified for your needs. You can add your own default signature and subject. Everything is customizable and only requires basic knowledge of html.

https://user-images.githubusercontent.com/11873738/233569381-8ec2f3b3-13f9-4559-9433-29e292b1c277.mp4

### Search Filters
SOMS makes it easy to find any order. You can search using a single field or any combination of fields. If you do not remember the order number you could even look it up by using the amount!

https://user-images.githubusercontent.com/11873738/233559069-75a1eb1a-eafa-4312-9541-daf3c92d367b.mp4

### Shortcuts
- Double clicking an order/row opens the attachment for that order.
- Pressing "ALT + ENTER" is the equivalent to pressing "SEARCH"
- Pressing "ALT + BACKSPACE" is the equivalent to pressing "CLEAR"
- Pressing "ALT + MOUSE1/LeftClick" is the equivalent to pressing "Modify" to modify an order.

https://user-images.githubusercontent.com/11873738/233567943-72299b17-771a-460b-9e67-560d7c386edf.mp4

### Creating a New Order
Creating a new order is very important. SOMS gives you the tools you need. When adding an attachment to the new order SOMS will copy and store it in its `/data` folder. This guarantees the access to that file for later use.
Please note: Adding an attachment to the new order is required.

https://user-images.githubusercontent.com/11873738/233559804-0e83916b-20e9-43d6-ba1c-8f5491196f58.mp4

### Modifying and Deleting an Order
Any order can be modified and/or deleted. When an order is modified if the attachment is the same it will be kept. However, you can change the attachment as well. When the order is deleted, the attachment is deleted as well. Please know that there is no way to restore deleted orders/attachments. You can also delete multiple orders simultaneously if that is something you want to do.

**NOTE:** The only field that cannot be modified is the order number as it is currently used to match your order attachment.

https://user-images.githubusercontent.com/11873738/233560381-de40490f-783b-4187-a5a5-b0bab78cb1c0.mp4

### Creating a New Supervisor
Creating a new supervisor validates the input using regex for all the fields. More work will be needed to make it more user friendly but for now it works and it is effective. 

https://user-images.githubusercontent.com/11873738/233562363-c47e5b2d-3dfd-4a76-8be9-8280f84cabea.mp4

### Creating a New Employee
Creating a new employee also allows the user to assign projects to that employee. Once the employee has one or more assigned projects, when a new order is being created, upon selecting the project the assigned employee for that project is automatically filled in.  For example: Here Claudio Emp is assigned Kendall TH. When adding a new order and upon selecting the company `Grand Homes` and project `Kendall TH` Claudio Emp is automatically selected as the employee.

**NOTE:** Projects can only be assigned to a single employee at this time. If a new employee is assigned a project then no other employee will have it. They are stripped from that project in the background.

https://user-images.githubusercontent.com/11873738/233564093-4ce7f774-9022-4533-b562-d8ddd2f786ff.mp4

### Creating a New Company (and Division)
Companies are your clients. Since SOMS is made for suppliers/subcontractors, it is expected to be working to more than one at the same time. Medium and Large sized companies have more than one division. Divisions are important as some projects may pertain to a division rather than another. This is it is required for every company to have at least one division.  

**NOTE:** Each division has its own accounts payable.

https://user-images.githubusercontent.com/11873738/233566101-f0a0f88b-a561-4329-ab80-c38f8f743731.mp4

### Creating a New Project
A company does not have projects by default, therefore, it is necessary to add projects. The New Project option allows you to select a company and one of its divisions and add a new project to it. You are also required to assign a default employee. When you create a new order for that project the employee is automatically selected but you are free to change it to a different employee. It is not a forced choice but a suggested one.

https://user-images.githubusercontent.com/11873738/233566383-1272acd8-211d-4541-b698-73533765b7b2.mp4


### Settings
The file /config.ini autosaves some settings while others are saved upon request or exection of certain triggers.
For example:
- The geometry of the main window is only saved when requested by going to the menu bar `Config>Store Current Layout as Default`
- The checkboxes to filter order status (Paid, Approved, etc...) are remembered upon restart. However, the last status (ON or OFF) of these checkboxes is only stored after performing a "Search".  

https://user-images.githubusercontent.com/11873738/233558732-72240c06-8c62-45e0-8b23-b4b8fc7b23cb.mp4

### Database Diagram
The database uses foreign keys and intersection tables to relate the tables. Please note that the primary keys are in yellow while the foreign keys are in blue.
![Database Relational Diagram](https://user-images.githubusercontent.com/11873738/232396864-d99b8a48-12c6-4991-ab57-0ae8f62d6bb6.png)

### Preventing Injection Attacks

All the input fields try to injection attacks checking the input from the entries and inserting them in the database through the use of placeholders. Since this program is a demo, it does NOT encrypt or protect the database in any way so please understand the work being done here is limited and mostly for demostrative purposes. Currently I am in a trade-off between time and features.
