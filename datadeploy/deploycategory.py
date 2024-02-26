import csv
import pymysql

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'strangedb',
    'password': 'as',
    'database': 'ceevee'
}

# CSV file path
csv_file = '../datadeploy/laptop_data.csv'

# Table name in the database
table_name = 'Laptop_data'

# Connect to the database
try:
    mydb = pymysql.connect(**db_config)
except pymysql.err.OperationalError as err:
    print("Error connecting to database:", err)
    exit()

mycursor = mydb.cursor()

# Get column names and data types from CSV
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    header_row = next(csv_reader)  # Skip the header row
    column_names = header_row
    column_defs = ', '.join([f"{name} VARCHAR(255)" for name in column_names])  # Assuming VARCHAR for all columns

# Create the table if it doesn't exist
mycursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {column_defs}
    )
""")

# Prepare the INSERT statement with placeholders for values
sql = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(column_names))})"

# Insert data from CSV to database
try:
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row again
        for row in csv_reader:
            mycursor.execute(sql, row)
    mydb.commit()
    print(f"Data copied from CSV to table '{table_name}' successfully!")
except pymysql.err.Error as err:
    print("Error copying data:", err)
    mydb.rollback()

mydb.close()
