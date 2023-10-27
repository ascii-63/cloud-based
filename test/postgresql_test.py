import psycopg2


class Person:
    name = ""
    age = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age


# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'server',
    'password': 'server',
    'host': 'localhost',
    'port': '5432'
}

John = Person('John', 30)
Alice = Person('Alice', 25)
Bob = Person('Bob', 35)

# Sample data to insert
data_to_insert = [
    (John.name, John.age),
    (Alice.name, Alice.age),
    (Bob.name, Bob.age)
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
