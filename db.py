import pyodbc

def get_db_connection():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=Bryna\SQLEXPRESS;DATABASE=SET_DATABASE_REAL;Trusted_Connection=yes;')

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the 'Users' table already exists
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        # Create the 'Users' table if it doesn't exist
        cursor.execute('CREATE TABLE Users (ID INT PRIMARY KEY, Name VARCHAR(255), HighScore INT)')
        print("Table 'Users' created successfully!")
    else:
        print("Table 'Users' already exists. No action taken.")

    conn.commit()
    conn.close()

# Call the create_table() function
create_table()

