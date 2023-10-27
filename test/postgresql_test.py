import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'server',
    'password': 'server',
    'host': 'localhost',
    'port': '5432'
}

# Sample data to insert
data_to_insert = [
    ('John', 30),
    ('Alice', 25),
    ('Bob', 35)
]

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object
    cursor = connection.cursor()

    # SQL statement to insert data into the table
    insert_query = "INSERT INTO test_table (name, age) VALUES (%s, %s)"

    # Loop through the data and execute the insert query for each record
    for record in data_to_insert:
        cursor.execute(insert_query, record)

    # Commit the changes to the database
    connection.commit()

    print("Data inserted successfully")

except (Exception, psycopg2.Error) as error:
    print(f"Error inserting data: {error}")

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
