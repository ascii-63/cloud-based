import pika
import os
import psycopg2
from datetime import datetime


env_file_path = '../.env'
image_dir_path = ''
db_params = {
    'dbname': 'event_db',
    'user': 'server',
    'password': 'server',
    'host': 'localhost',
    'port': '5432'
}
event_table = 'event_table'


# Get the timestamp of the event
def getTimestampFromEvent(event):
    timestamp = datetime[0, 0, 0, 0, 0, 0]
    return timestamp


# Get image path go with this event
def getImagePathFromEvent(event):
    image_path = ''
    return image_path


# Insert event to database
def insert_db(event):
    timestamp = getTimestampFromEvent(event)
    image_path = getImagePathFromEvent(event)

    # Data to insert to database
    data_to_insert = (timestamp, event, image_path)
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)

        # Create a cursor object
        cursor = connection.cursor()

        # SQL statement to insert data into the table
        insert_query = "INSERT INTO " + event_table + \
            " (timestamp, event, image_path) VALUES (%s, %s, %s)"

        cursor.execute(insert_query, data_to_insert)

    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data: {error}")


# Read and parse the .env file
with open(env_file_path) as f:
    for line in f:
        if line.strip() and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

# Read the AMQP server configuration from the environment variables
amqp_url = os.environ.get('AMQP_URL')
queue_name = os.environ.get('QUEUE')

# Create a connection to the AMQP server using the configuration
connection_parameters = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=queue_name)


# Define a callback function to process incoming messages
def callback(ch, method, properties, body):
    # Decode the message from bytes to string
    decoded_message = body.decode('utf-8')
    print(f"{decoded_message}")

    insert_db(decoded_message)

    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up the consumer and specify the callback function
channel.basic_consume(
    queue=queue_name, on_message_callback=callback)
# queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages. To exit, press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
