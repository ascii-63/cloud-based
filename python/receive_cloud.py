import pika
import os

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
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up the consumer and specify the callback function
channel.basic_consume(
    queue=queue_name, on_message_callback=callback)
    # queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages. To exit, press CTRL+C')
# channel.start_consuming()
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
