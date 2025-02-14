import sqlite3
import pandas as pd

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('data/data.db')  # Path to your SQLite database
    return conn

# Function to fetch all table names from the database
def get_tables():
    conn = connect_db()
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    conn.close()
    return tables

# Function to fetch the data from a specific table
def get_table_data(table_name):
    conn = connect_db()
    query = f"SELECT * FROM {table_name};"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Main function to display tables and their rows
def display_db():
    # Get list of all tables in the database
    tables = get_tables()
    print("Tables in the database:\n")
    for table in tables['name']:
        print(f"Table: {table}")
        table_data = get_table_data(table)
        print(table_data.to_string(index=False))  # Print the table data without the index
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    display_db()
