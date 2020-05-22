import os

import mysql.connector
from mysql.connector import errorcode

DB_NAME = "mydata"

cursor = ""
cnx = mysql.connector.connect(user='root', password='mysql', host='localhost')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
    print("Database already exists and in use")
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

TABLES = {}


TABLES['USERS'] = ("CREATE TABLE `USERS` ("
                   "FIRSTNAME varchar(64) NOT NULL,"
                   " LASTNAME varchar(64) NOT NULL,"
                   " USERNAME varchar(64) NOT NULL,"
                   " EMAIL varchar(64) NOT NULL,"
                   " PASSWORD varchar(64) NOT NULL,"
                   " PHONE VARCHAR(64) NOT NULL"
                   " );")

TABLES['SERVICE_PROVIDER'] = ("CREATE TABLE SERVICE_PROVIDER("
                   "PROVIDER_NAME VARCHAR(50) NOT NULL,"
                   " PHONE_NUMBER VARCHAR(50) NOT NULL,"
                   " EMAIL VARCHAR(50) NOT NULL,"
                   " AGENT_NAME VARCHAR(50) NOT NULL,"
                   " PRIMARY KEY (PROVIDER_NAME));")

TABLES['SPARE_PARTS'] = ("CREATE TABLE SPARE_PARTS("
                         "SPARE_NAME VARCHAR(50) NOT NULL,"
                         " SERIAL_NUMBER VARCHAR(50) NOT NULL,"
                         " QUANTITY INT NOT NULL,"
                         " SPARE_PRICE FLOAT NOT NULL,"
                         " SPARE_MANUFACTURER VARCHAR(300) NOT NULL,"
                         " PRIMARY KEY (SERIAL_NUMBER));")

TABLES['EQUIPMENT'] = ("CREATE TABLE EQUIPMENT("
                       " ID VARCHAR(50) NOT NULL,"
                       " DEPARTMENT VARCHAR(50) NOT NULL,"
                       " MANUFACTURER VARCHAR(50) NOT NULL,"
                       " MODEL VARCHAR(50) NOT NULL,"
                       " SERIAL_NUMBER VARCHAR(50) NOT NULL,"
                       " MANUFACTURER_COUNTRY VARCHAR(50) NOT NULL,"
                       " INDATE VARCHAR(50) NOT NULL,"
                       " OPERATION_DATE VARCHAR(50) NOT NULL,"
                       " WARRANTY_PERIOD VARCHAR(50) NOT NULL,"
                       " SUPPLIER VARCHAR(50) NOT NULL,"
                       " PRICE FLOAT NOT NULL,"
                       " MAINTAINANCE_COMPANY VARCHAR(50) NOT NULL,"
                       " MAINTAINANCE_CONTRACT_TYPE VARCHAR(50) NOT NULL,"
                       " START_END_CONTRACT_DATE VARCHAR(50) NOT NULL,"
                       " RECIPIENT_NAME VARCHAR(50) NOT NULL,"
                       " RECIPIENT_PHONE VARCHAR(50) NOT NULL,"
                       " PRIMARY KEY (SERIAL_NUMBER));")

for table_name in TABLES:
    table_description = TABLES[table_name]
    print(table_name)
    try:
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
