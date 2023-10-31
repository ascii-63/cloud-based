import pika
import os
import time

env_file_path = '../.env'

# Read and parse the .env file
with open(env_file_path) as f:
    for line in f:
        if line.strip() and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

# Read the AMQP server configuration from the environment variables
amqp_url = os.environ.get('AMQP_URL')
queue_name = os.environ.get('QUEUE')

# Create a connection to the AMQP server using the configuration and declare a queue
connection_parameters = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue=queue_name)

# Send messages in a loop
for i in range(100):
    message_body = f"Message {i}"

    # Publish the message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message_body
    )

    print(f"[x] Sent message: {message_body}")

    time.sleep(1)  # Delay between messages

# Close the connection
connection.close()
