import psycopg2
from datetime import datetime


# Database connection parameters
db_params = {
    'dbname': 'event_db',
    'user': 'server',
    'password': 'server',
    'host': 'localhost',
    'port': '5432'
}
event_table = 'event_table'

custom_timestamp = datetime(2023, 10, 30, 17, 20, 0)

# Sample data to insert
data_to_insert = [
    (custom_timestamp,
     '{ \"timestamp\": \"100\", \"event\": {\"position\": [192,168,1],\"object\": \"Human\"},\"image_ID\": \"100\"}', './image/100.png'),
    (custom_timestamp,
     '{ \"timestamp\": \"101\", \"event\": {\"position\": [192,168,1],\"object\": \"Human\"},\"image_ID\": \"101\"}', './image/101.png'),
    (custom_timestamp,
     '{ \"timestamp\": \"102\", \"event\": {\"position\": [192,168,1],\"object\": \"Human\"},\"image_ID\": \"102\"}', './image/102.png'),
]

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object
    cursor = connection.cursor()

    # SQL statement to insert data into the table
    insert_query = "INSERT INTO " + event_table + \
        " (timestamp, event, image_path) VALUES (%s, %s, %s)"

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
