Kagwandu Enterprises Database Setup and Query
This project demonstrates how to interact with a PostgreSQL database uisng python and SQL hosted on AWS RDS. It involves creating an RDS instance, setting up three tables (brands, models, sales), and inserting data into them. The data is read from CSV files stored in an S3 bucket and inserted into the tables. Additionally, there is a script to query the data from all three tables.

Overview
Database Creation: Creates an AWS RDS PostgreSQL database.

Table Setup: Creates three tables (brands, models, sales) in the PostgreSQL database.

Data Insertion: Inserts data into the tables from CSV files stored in an S3 bucket.

Data Querying: Queries the inserted data from the three tables and prints the results.

