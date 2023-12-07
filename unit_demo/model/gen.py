import json
import uuid
import random
from datetime import datetime
import time
import pika

##############################################################


def generate_random_message():
    message_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print(timestamp)

    topleftx = random.randint(0, 640)
    toplefty = random.randint(0, 640)
    bottomrightx = random.randint(0, 640)
    bottomrighty = random.randint(0, 640)

    id = str(uuid.uuid4())
    typee = random.choice(["moving", "stopped"])

    message = {
        "messageid": message_id,
        "@timestamp": timestamp,
        "place": {
            "id": "1",
            "name": "XYZ",
            "type": "garage",
            "location": {
                "lat": 21.005453,
                "lon": 105.8451935,
                "alt": 48.15574793
            }
        },
        "sensor": {
            "id": "CAMERA_ID",
            "type": "Camera",
            "description": "Camera description",
            "location": {
                "lat": 21.005453,
                "lon": 105.8451935,
                "alt": 48.15574793
            }
        },
        "object": {
            "id": "18446744073709551615",
            "bbox": {
                "topleftx": topleftx,
                "toplefty": toplefty,
                "bottomrightx": bottomrightx,
                "bottomrighty": bottomrighty
            },
            "location": {
                "lat": 21.005453,
                "lon": 105.8451935,
                "alt": 48.15574793
            }
        },
        "event": {
            "id": id,
            "type": typee
        },
        "imageURL": "",
        "videoURL": ""
    }

    return message, timestamp

##############################################################


# Define the AMQP server connection parameters, including login credentials
credentials = pika.PlainCredentials('guest', 'guest')
connection_parameters = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='/',
    credentials=credentials
)

# Create a connection to the AMQP server
connection = pika.BlockingConnection(connection_parameters)

# Create a channel
channel = connection.channel()

# Declare the queue you want to send messages to
queue_name = 'event'  # Modify with your queue name
channel.queue_declare(queue=queue_name)

for _ in range(10):
    random_message, timestamp = generate_random_message()
    # Publish the message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=random_message
    )
    print(f"Sent message: {random_message}")
    time.sleep(1)  # Delay between messages

# Close the connection
connection.close()
