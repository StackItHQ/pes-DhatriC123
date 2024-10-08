import mysql.connector

# Function to create a MySQL connection
def get_mysql_connection():
    connection = mysql.connector.connect(
        host='localhost',   # Change to your MySQL host
        user='root',  # Replace with your MySQL username
        password='DiapB2002',  # Replace with your MySQL password
        database='superjoin'  # Replace with your database name
    )
    return connection

# Function to read data from the MySQL database
def read_mysql_data(query):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Function to write data to MySQL database
def write_mysql_data(query, values):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    # Update data in MySQL
def update_mysql_data(query, values):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

# Delete data in MySQL
def delete_mysql_data(query, params):
    connection = get_mysql_connection()  # Your connection details here
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()
