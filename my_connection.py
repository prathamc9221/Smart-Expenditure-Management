# [3:59 AM, 2/18/2024] Swapnil Mane CS Bing: integral-vim-230317:us-central1:sem-hack-bu
# [3:59 AM, 2/18/2024] Swapnil Mane CS Bing: 34.123.254.183
# [3:59 AM, 2/18/2024] Swapnil Mane CS Bing: SQL Instance 

# user id: sem-hack-bu

# SemHack

import mysql.connector

# GCP MySQL instance details
gcp_mysql_config = {
    'user': 'root',
    'password': 'SemHack',
    'host': '34.123.254.183',
    'database': 'myexpense',
    'raise_on_warnings': True,
}

import os

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = "integral-vim-230317:us-central1:sem-hack-bu"  # e.g. 'project:region:instance'
    db_user = "root"  # e.g. 'my-db-user'
    db_pass = 'SemHack'  # e.g. 'my-db-password'
    db_name = 'myexpense'  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector(ip_type)

    # def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name,
    )
    return conn

    # pool = sqlalchemy.create_engine(
    #     "mysql+pymysql://",
    #     creator=getconn,
    #     # ...
    # )
    # return pool
    


def insert_into_customer(data):
    try:
        connection = connect_with_connector()
        # Create a cursor object
        cursor = connection.cursor()

        # SQL query for inserting a new record
        insert_query = "INSERT INTO Customer (Full_Name, email_address, password, Income_amount, Saving_Percentage) VALUES (%s, %s, %s, %s, %s)"

        # Data to be inserted
        # data = ('Jane Doe', 'jane@gmail.com', 'newpassword', 60000.00, 8.75)

        # Execute the query
        cursor.execute(insert_query, data)

        # Commit the changes
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# data = ('Anagha', 'aghate@gmail.com', 'newpassword', 6000.00, 10.75)
# insert_into_customer(connection, data)

def insert_into_transactions(data):
    try:
        connection = connect_with_connector()
        # Create a cursor object
        cursor = connection.cursor()

        # SQL query for inserting a new record
        insert_query = "INSERT INTO Transactions (Date, Description, Category, Cost, Currency, customer_id) VALUES (%s, %s, %s, %s, %s, %s)"
        # Data to be inserted
        # data = ('Jane Doe', 'jane@gmail.com', 'newpassword', 60000.00, 8.75)

        # Execute the query
        cursor.execute(insert_query, data)

        # Commit the changes
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def select_all(query):
    connection = connect_with_connector()
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # SQL query for selecting data
        # select_query = "SELECT * FROM " + table_name

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        return rows

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# print(select_all(connection, "Customer"))

def update(table_name, columns, data, condition):
    connection = connect_with_connector()
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # SQL query for updating data
        update_query = "UPDATE " + table_name + " SET " + columns + " = %s WHERE "+ condition
        
        # New data and condition
        new_value = 'new_value'
        condition_value = 'condition_value'

        # Execute the query
        cursor.execute(update_query, (new_value, condition_value))

        # Commit the changes
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
