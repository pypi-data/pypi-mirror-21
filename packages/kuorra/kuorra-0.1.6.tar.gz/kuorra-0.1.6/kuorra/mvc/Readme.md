# kuorra

### Introduction

Kuorra is a Web.py Microframework Frontend, use kuorra to create a MVC skeleton for work with Web.py, MySQL and Heroku App.

### Funtions

+ Script for create a demo DB.

+ Config one DB conection.

+ Create a products **Controller**.

  - *Index*
  - *View*
  - *Edit*
  - *Delete*
  - *Insert*

+ Create a products **Model**.

  - *get_all_products*
  - *get_product*
  - *delete_product*
  - *insert_product*
  - *edit_product*

+ Create a products **Views**:

  - *Index*
  - *View*
  - *Edit*
  - *Delete*
  - *Insert*
  - *Master* (Web Template)

+ Create a products API.

  - *Show all products* (GET)
  - *Search one product* (POST)

7. Active a SSL connection


### Use

+ Create new project

  - **kuorra new project_name**

+ Deploy project (into de project folder)

  - **kuorra dep**

+ Info
  - **kuorra info**

### Configuration

+ The new project have a demo database  called **acme_store_mvc**, with a products table.

+ The database script is written in the file **data + schema.sql**.

+ Connect to MySQL server using *mysql cli*, *mysql workbench* or any other application and execute the script **schema.sql** for create the DB.

+ In the file **application + models + model_products.py** modify the connection parameters

  - **db_host** = 'localhost'
  - **db_name** = 'acme_store_mvc'
  - **db_user** = 'your user name'
  - **db_pw** = 'your password'

+ Into de folder where is the **app.py** file execute **kuorra dep** for deploy de WebApp.

+ For stop de server press **Ctrl + C**.