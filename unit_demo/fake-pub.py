import pika
import json
import time

# Replace these values with your AMQP broker connection details
AMQP_HOST = 'gerbil-01.rmq.cloudamqp.com'
AMQP_PORT = 5672
AMQP_USERNAME = 'slbnkadk'
AMQP_PASSWORD = 'yjICj6LodkqaxgCG2rDIjvqJQ5Ihoo_u'
AMQP_QUEUE_NAME = 'message'
AMQP_VHOST = 'slbnkadk'

# Example JSON message
example_message = {
    "message_id": "0000-0001-0002-000000",
    "timestamp": "2023-12-25T07:38:42.491",
    "location": {
        "id": "0000",
        "lat": 21.005453,
        "lon": 105.8451935,
        "alt": 48.15574793
    },
    "model": {
        "id": "0001",
        "description": "Model ID 0001: Human and Vehicle detection"
    },
    "camera": {
        "id": "0002",
        "type": "RGB",
        "description": "Cam ID 0002: RGB Camera"
    },
    "number_of_objects": 3,
    "object_list": [
        {
            "Human": {
                "id": "01",
                "gender": "Male",
                "age": "20",
                "bbox": {
                    "topleftx": 32,
                    "toplefty": 0,
                    "bottomrightx": 177,
                    "bottomrighty": 0
                }
            }
        },
        {
            "Human": {
                "id": "02",
                "gender": "Female",
                "age": "30",
                "bbox": {
                    "topleftx": 35,
                    "toplefty": 0,
                    "bottomrightx": 145,
                    "bottomrighty": 0
                }
            }
        },
        {
            "Vehicle": {
                "id": "03",
                "type": "Personal car",
                "brand": "BMW",
                "color": "Black",
                "Licence": "29A-12345",
                "bbox": {
                    "topleftx": 345,
                    "toplefty": 0,
                    "bottomrightx": 108,
                    "bottomrighty": 20
                }
            }
        }
    ],
    "number_of_events": 2,
    "event_list": [
        {
            "human_event": {
                "object_id": "01",
                "type": "EVENT_HUMAN_RUN"
            },
            "vehicle_event": {
                "object_id": "03",
                "type": "EVENT_VEHICLE_PARK"
            }
        }
    ],
    "image_URL": "https://example.com",
    "video_URL": "https://example.com"
}


def publish_message(channel, message):
    channel.basic_publish(
        exchange='',
        routing_key=AMQP_QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )
    print(f" [x] Sent: {message}")


def main():
    # Establish connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=AMQP_HOST,
        port=AMQP_PORT,
        credentials=pika.PlainCredentials(
            username=AMQP_USERNAME, password=AMQP_PASSWORD,),
        virtual_host=AMQP_VHOST
    ))
    channel = connection.channel()

    # Declare the queue (create if not exists)
    channel.queue_declare(queue=AMQP_QUEUE_NAME, durable=True)

    try:
        while True:
            publish_message(channel, example_message)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print(" [x] Interrupted. Closing connection.")
        connection.close()


if __name__ == '__main__':
    main()
