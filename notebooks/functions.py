# imports
import requests
import pandas as pd
import os
import sqlite3

   
def get_sql_table(database, table_name):
    """ 
    gets an sql table from a provided database.

    Parameters:
    database (string): the SQL database
    table_name (string): the SQL table name that you wish to retrieve from the database

    Returns:
    DataFrame: the sql table as a dataframe
    """

    con_string = f'../data/{database}.db'
    con = sqlite3.connect(con_string) 
    query = f"""
        SELECT *
        FROM {table_name}
    """
    df = pd.read_sql_query(query, con)
    con.close()
    if table_name == 'yelp':
        df['rating'] = df['rating'] * 2
    return df