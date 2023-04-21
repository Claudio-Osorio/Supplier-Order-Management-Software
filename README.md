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

### Database Diagram
The database uses foreign keys and intersection tables to relate the tables. Please note that the primary keys are in yellow while the foreign keys are in blue.
![Database Relational Diagram](https://user-images.githubusercontent.com/11873738/232396864-d99b8a48-12c6-4991-ab57-0ae8f62d6bb6.png)

## Functionality

### Settings
The file /config.ini autosaves some settings while others are saved upon request or exection of certain triggers.
For example:
- The geometry of the main window is only saved when requested by going to the menu bar `Config>Store Current Layout as Default`
- The checkboxes to filter order status (Paid, Approved, etc...) are remembered upon restart. However, the last status (ON or OFF) of these checkboxes is only stored after performing a "Search".  

https://user-images.githubusercontent.com/11873738/233558732-72240c06-8c62-45e0-8b23-b4b8fc7b23cb.mp4

### Search Filters
SOMS makes it easy to find any order. You can search using a single field or any combination of fields. If you do not remember the order number you could even look it up by using the amount!

https://user-images.githubusercontent.com/11873738/233559069-75a1eb1a-eafa-4312-9541-daf3c92d367b.mp4

### Creating a New Order
Creating a new order is very important. SOMS gives you the tools you need. When adding an attachment to the new order SOMS will copy and store it in its `/data` folder. This guarantees the access to that file for later use.
Please note: Adding an attachment to the new order is required.

https://user-images.githubusercontent.com/11873738/233559804-0e83916b-20e9-43d6-ba1c-8f5491196f58.mp4

### Modifying and Deleting an Order
Any order can be modified and/or deleted. When an order is modified if the attachment is the same it will be kept. However, you can change the attachment as well. When the order is deleted, the attachment is deleted as well. Please know that there is no way to restore deleted orders/attachments. You can also delete multiple orders simultaneously if that is something you want to do.

NOTE: The only field that cannot be modified is the order number as it is currently used to match your order attachment.

https://user-images.githubusercontent.com/11873738/233560381-de40490f-783b-4187-a5a5-b0bab78cb1c0.mp4

