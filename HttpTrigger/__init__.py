import logging

import azure.functions as func

import os
import pyodbc
import struct

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    server="kl-sqlserver.database.windows.net"
    database="test"
    driver="{ODBC Driver 17 for SQL Server}"
    query="SELECT * FROM dbo.users"
    # username = 'name' 
    # password = 'pass'
    db_token = ''
    connection_string = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+database

    if os.getenv("MSI_SECRET"):
        conn = pyodbc.connect(connection_string+';Authentication=ActiveDirectoryMsi')
        
    else:
        SQL_COPT_SS_ACCESS_TOKEN = 1256

        exptoken = b''
        for i in bytes(db_token, "UTF-8"):
            exptoken += bytes({i})
            exptoken += bytes(1)

        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken
        conn = pyodbc.connect(connection_string, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct })
        # conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute(query) 
    row = cursor.fetchone()

    while row:
        print(row[0])
        row = cursor.fetchone()

    return func.HttpResponse(
            'Success',
            status_code=200
    )
