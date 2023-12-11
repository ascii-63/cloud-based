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
remote_amqp_url = os.environ.get('AMQP_URL')
remote_queue_name = os.environ.get('QUEUE')


# Receive message from the local AMQP server
def receive_message():
    # Define the local AMQP server connection parameters
    local_connection_parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest')
    )

    # Create a connection to the local AMQP server
    local_connection = pika.BlockingConnection(local_connection_parameters)
    local_channel = local_connection.channel()

    # Declare the queue to receive messages from
    local_queue_name = 'event'
    local_channel.queue_declare(queue=local_queue_name)

    # Define a callback function to process received messages
    def local_callback(ch, method, properties, body):
        # Send the received message to the remote AMQP server
        send_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up the consumer and specify the callback function
    local_channel.basic_consume(
        queue=local_queue_name, on_message_callback=local_callback)
        # queue=local_queue_name, on_message_callback=local_callback, auto_ack=True)

    print('Waiting for messages from the local AMQP server. To exit, press CTRL+C')
    # local_channel.start_consuming()
    try:
        local_channel.start_consuming()
    except KeyboardInterrupt:
        local_channel.stop_consuming()


# Send message to the remote AMQP server
def send_message(message):
    # Create a connection to the remote AMQP server using the configuration
    remote_connection_parameters = pika.URLParameters(remote_amqp_url)
    remote_connection = pika.BlockingConnection(remote_connection_parameters)
    remote_channel = remote_connection.channel()

    # Publish the received message to the remote queue
    remote_channel.basic_publish(
        exchange='',
        routing_key=remote_queue_name,
        body=message
    )

    print(f"Sent message to the remote AMQP server: {message}")

    # Close the connection to the remote AMQP server
    remote_connection.close()


if __name__ == '__main__':
    receive_message()
