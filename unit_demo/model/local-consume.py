import pika


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
        decoded_message = body.decode('utf-8')
        print(f"{decoded_message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up the consumer and specify the callback function
    local_channel.basic_consume(
        queue=local_queue_name, on_message_callback=local_callback)

    print('Waiting for messages from the local AMQP server. To exit, press CTRL+C')

    try:
        local_channel.start_consuming()
    except KeyboardInterrupt:
        local_channel.stop_consuming()


if __name__ == '__main__':
    receive_message()
