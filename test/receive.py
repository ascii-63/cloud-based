import pika

# Define the AMQP server connection parameters, including login credentials
credentials = pika.PlainCredentials('slbnkadk', 'yjICj6LodkqaxgCG2rDIjvqJQ5Ihoo_u')
connection_parameters = pika.ConnectionParameters(
    host='gerbil.rmq.cloudamqp.com',
    port=5672,
    virtual_host='slbnkadk',
    credentials=credentials
)

# Create a connection to the AMQP server
connection = pika.BlockingConnection(connection_parameters)

# Create a channel
channel = connection.channel()

# Declare the queue you want to receive messages from
queue_name = 'event'  # Modify with your queue name
channel.queue_declare(queue=queue_name)

# Define a callback function to process incoming messages
def callback(ch, method, properties, body):
    print(f"Received message: {body}")

# Set up the consumer and specify the callback function
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
