import pika
import time

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

# Declare the queue you want to send messages to
queue_name = 'event'  # Modify with your queue name
channel.queue_declare(queue=queue_name)

# Send messages in a loop
for i in range(100):  # Adjust the number of messages as needed
    message_body = f"Message {i}"  # Include the index in the message

    # Publish the message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message_body
    )

    print(f"Sent message: {message_body}")

    time.sleep(1)  # Delay for 2 seconds between messages

# Close the connection
connection.close()
