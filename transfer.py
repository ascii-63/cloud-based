from google.cloud import storage

import sys
import os
import pika
import json
from datetime import datetime, timedelta
import time


IMAGE_EXTENTION = '.jpg'
VIDEO_EXTENTION = '.mp4'

ENV_FILE_PATH = '.env'
CFG_FILE_PATH = 'message_config.txt'

PERSON_RENAME = 'Human'
VEHICLE_RENAME = 'Vehicle'

# In the person object of model message, these field index is empty/not useable
PERSON_MESSAGE_FIELD_REMOVE_LIST = [6, 10, 11]

COLON_UNICODE = '%3A'

##################################

remote_amqp_url = None
remote_queue_name = None

bucket_name = None

local_image_dir = None
local_video_dir = None
cloud_image_dir = None
cloud_video_dir = None

url_start = 'https://storage.googleapis.com/'
image_url_start = None
video_url_start = None

##################################

location_id = None
location_lat = None
location_lon = None
location_alt = None

model_id = None
model_description = None

camera_id = None
camera_type = None
camera_description = None

prev_message_id = None

##################################


class Object:
    def __init__(self, id, topleftx, toplefty, bottomrightx, bottomrighty):
        self.id = str(id)
        self.topleftx = float(topleftx)
        self.toplefty = float(toplefty)
        self.bottomrightx = float(bottomrightx)
        self.bottomrighty = float(bottomrighty)


class Person(Object):
    def __init__(self, id, topleftx, toplefty, bottomrightx, bottomrighty, obj_type, gender, age, hair_color, confidence):
        super().__init__(id, topleftx, toplefty, bottomrightx, bottomrighty)
        self.gender = gender
        self.age = age
        self.hair_color = hair_color
        self.confidence = confidence


class Vehicle(Object):
    def __init__(self, id, topleftx, toplefty, bottomrightx, bottomrighty, type, brand, color, licence, confidence):
        super().__init__(id, topleftx, toplefty, bottomrightx, bottomrighty)
        self.type = type
        self.brand = brand
        self.color = color
        self.licence = licence
        self.confidence = confidence


##################################
# SAMPLE MESSAGE
sample_raw_message = '{"version": "4.0","id": "0","@timestamp": "2023-12-25T09:02:45.820Z","sensorId": "","objects": ["18446744073709551615|1126.77|447.984|1276.23|717.798|Person|#|Male|20|Black|||0.873829"]}'

##################################


def envFileParser():
    """Read and parse the .env file"""

    global remote_amqp_url, remote_queue_name
    global bucket_name
    global local_image_dir, local_video_dir, cloud_image_dir, cloud_video_dir
    global url_start, image_url_start, video_url_start

    with open(ENV_FILE_PATH) as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

    #############################
    remote_amqp_url = os.environ.get('AMQP_URL')
    remote_queue_name = os.environ.get('QUEUE')

    bucket_name = os.environ.get('BUCKET')

    local_image_dir = os.environ.get('LOCAL_IMAGE_DIR')
    local_video_dir = os.environ.get('LOCAL_VIDEO_DIR')
    cloud_image_dir = os.environ.get('CLOUD_IMAGE_DIR')
    cloud_video_dir = os.environ.get('CLOUD_VIDEO_DIR')

    image_url_start = url_start + bucket_name + '/' + cloud_image_dir + '/'
    video_url_start = url_start + bucket_name + '/' + cloud_video_dir + '/'

    #############################

    if (
        remote_amqp_url is None
        or remote_queue_name is None
        or bucket_name is None
        or local_image_dir is None
        or local_video_dir is None
        or cloud_image_dir is None
        or cloud_video_dir is None
        or image_url_start is None
        or video_url_start is None
    ):
        return False
    return True


def configFileParser():
    """Read and parse the message config file"""

    global location_id, location_lat, location_lon, location_alt
    global model_id, model_description
    global camera_id, camera_type, camera_description
    global prev_message_id

    #############################
    try:
        with open(CFG_FILE_PATH, 'r') as file:
            for line in file:
                key, value = line.strip().split('=', 1)

                if key == 'LOCATION_ID':
                    location_id = value
                elif key == 'LOCATION_LAT':
                    location_lat = float(value)
                elif key == 'LOCATION_LON':
                    location_lon = float(value)
                elif key == 'LOCATION_ALT':
                    location_alt = float(value)

                elif key == 'MODEL_ID':
                    model_id = value
                elif key == 'MODEL_DESCRIPTION':
                    model_description = value

                elif key == 'CAMERA_ID':
                    camera_id = value
                elif key == 'CAMERA_TYPE':
                    camera_type = value
                elif key == 'CAMERA_DESCRIPTION':
                    camera_description = value

                elif key == 'PREV_MESSAGE_ID':
                    prev_message_id = int(value)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)

    #############################

    if (
        location_id is None
        or location_lat is None
        or location_lon is None
        or location_alt is None
        or model_id is None
        or model_description is None
        or camera_id is None
        or camera_type is None
        or camera_description is None
        or prev_message_id is None
    ):
        return False
    return True


def searchFileInDirectory(_directory, _file_name):
    """
    Search for a file in a directory.

    Parameters:
    - _directory: The directory to search in.
    - _file_name: The name of the file to search for.

    Returns:
    - True if the file is found, False otherwise.
    """
    # Get the list of files in the directory
    try:
        files_in_directory = os.listdir(_directory)
    except Exception as e:
        print(f"Some error: {e}")
        return False

    # Check if the file is in the list
    if _file_name in files_in_directory:
        return True
    else:
        return False


def getTimestampFromMessage(_message):
    """Get the timestamp of the original message"""

    data = json.loads(_message)
    timestamp_str = data.get('@timestamp')

    # Pop the 'Z' in the original timestamp string
    new_ts_str = timestamp_str[:-1]
    return new_ts_str


def convertUTC0ToUTC7(timestamp):
    """Convert ts str from UTC+0 to UTC+7"""

    dt_utc0 = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')

    utc0 = timedelta(hours=0)
    utc7 = timedelta(hours=7)
    dt_utc7 = dt_utc0 + (utc7 - utc0)

    timestamp_utc7 = dt_utc7.strftime('%Y-%m-%dT%H:%M:%S.%f')
    final_timestamp = timestamp_utc7[0:-4]

    return final_timestamp


def getImageURL(_timestamp_str):
    """Get Image Public URL from Google Storage with a specific timestamp"""

    global image_url_start
    image_url = image_url_start
    
    timestamp_str = str(_timestamp_str)
    timestamp_str.replace(':', COLON_UNICODE)
    image_url = image_url + timestamp_str + IMAGE_EXTENTION

    return image_url


def getVideoURL(_timestamp_str):
    """Get Image Public URL from Google Storage with a specific timestamp"""
    return None


def singleBlobUpload(_bucket_name, _source_file_name, _destination_blob):
    """
    Uploads a file to the bucket:
    _bucket_name: The ID of your GCS bucket
    _source_file_name: The path to the file to upload
    _destination_blon: The path to the file in GCS bucket
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(_bucket_name)
    destination_blob_name = _destination_blob
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    try:
        blob.upload_from_filename(
            _source_file_name, if_generation_match=generation_match_precondition)
    except Exception as e:
        print(f"Error when upload {_source_file_name} to bucket: {e}")
        return False

    print(f"File {_source_file_name} uploaded to bucket: {destination_blob_name}")
    return True


def sendImageAndVideo(_message):
    """Send image and video match with timestamp in message"""

    img_up_res = False
    vid_up_res = False

    timestamp = getTimestampFromMessage(_message)
    new_timestamp = convertUTC0ToUTC7(timestamp)
    timestamp = new_timestamp

    if (timestamp != None):
        local_image_name = timestamp + 'Z' + IMAGE_EXTENTION
        local_video_name = timestamp + 'Z' + VIDEO_EXTENTION
        cloud_image_name = timestamp + IMAGE_EXTENTION
        cloud_video_name = timestamp + VIDEO_EXTENTION
        print(f"Local image name: {local_image_name}")
        print(f"Cloud image name: {cloud_image_name}")

        #############################

        if searchFileInDirectory(local_image_dir, local_image_name):
            image_path = local_image_dir + '/' + local_image_name
            destination_blob_img = cloud_image_dir + '/' + cloud_image_name
            if singleBlobUpload(bucket_name, image_path, destination_blob_img):
                img_up_res = True
        else:
            print(f"The image: {local_image_name} is not found.")

        #############################

        if searchFileInDirectory(local_image_dir, local_video_name):
            video_path = local_video_dir + '/' + local_video_name
            destination_blob_vid = cloud_video_dir + '/' + cloud_video_name
            if singleBlobUpload(bucket_name, video_path, destination_blob_vid):
                vid_up_res = True
        else:
            print(f"The video: {local_video_name} is not found.")
    else:
        print(f"No timestamp found in message.")
        return False, False

    return img_up_res, vid_up_res


def rawMessageParsing(_raw_msg):
    """
    Parse the raw JSON message from model.
    Return timestamp in str (without 'Z'), and list of objects.
    """

    data = json.loads(_raw_msg)

    timestamp_str = data["@timestamp"]
    new_ts_str = timestamp_str[:-1]

    objects_data = data["objects"]
    objects_list = []

    for object_str in objects_data:
        fields = object_str.split('|')
        object_type = fields[5]

        if object_type == 'Person':
            fields.pop(PERSON_MESSAGE_FIELD_REMOVE_LIST[0])
            fields.pop(PERSON_MESSAGE_FIELD_REMOVE_LIST[1] - 1)
            fields.pop(PERSON_MESSAGE_FIELD_REMOVE_LIST[2] - 2)

            person = Person(*fields)
            objects_list.append(person)
        elif object_type == 'Vehicle':
            pass
            # vehicle = Vehicle(*fields)
            # objects_list.append(vehicle)

    return new_ts_str, objects_list


def cloudMessageGenerate(_raw_msg):
    """
    Parse the model message, return the cloud message in JSON format
    """

    global location_id, location_lat, location_lon, location_alt
    global model_id, model_description
    global camera_id, camera_type, camera_description
    global prev_message_id

    timestamp_str, objects_list = rawMessageParsing(_raw_msg)
    num_obj = len(objects_list)
    num_event = 0

    if prev_message_id > 999999:
        prev_message_id %= 1000000
    message_id = location_id + '-' + model_id + \
        '-' + camera_id + '-' + '{:06d}'.format(prev_message_id)
    prev_message_id += 1

    image_url = getImageURL(timestamp_str)
    video_url = getVideoURL(timestamp_str)

    ###########################

    message = {
        "message_id": message_id,
        "timestamp": timestamp_str,
        "location": {
            "id": location_id,
            "lat": location_lat,
            "lon": location_lon,
            "alt": location_alt
        },
        "model": {
            "id": model_id,
            "description": model_description
        },
        "camera": {
            "id": camera_id,
            "type": camera_type,
            "description": camera_description
        },
        "number_of_objects": num_obj,
        "object_list": [],
        "number_of_events": num_event,
        "event_list": [],
        "image_URL": image_url,
        "video_URL": video_url
    }

    ###########################

    obj_idx = 0
    for obj in objects_list:
        if (isinstance(obj, Person)):
            message["object_list"].append({
                PERSON_RENAME: {
                    "id": '{:02d}'.format(obj_idx),
                    "gender": obj.gender,
                    "age": obj.age,
                    "bbox": {
                        "topleftx": obj.topleftx,
                        "toplefty": obj.toplefty,
                        "bottomrightx": obj.bottomrightx,
                        "bottomrighty": obj.bottomrighty
                    }
                }
            })
            obj_idx += 1
        elif (isinstance(obj, Vehicle)):
            message["object_list"].append({
                VEHICLE_RENAME: {
                    "id": '{:02d}'.format(obj_idx),
                    "type": obj.type,
                    "brand": obj.brand,
                    "color": obj.color,
                    "licence": obj.licence,
                    "bbox": {
                        "topleftx": obj.topleftx,
                        "toplefty": obj.toplefty,
                        "bottomrightx": obj.bottomrightx,
                        "bottomrighty": obj.bottomrighty
                    }
                }
            })
            obj_idx += 1
        else:
            break

    if (obj_idx != num_obj):
        return ''

    return json.dumps(message)


def sendMessage(_message):
    """Send message to the remote AMQP server"""

    global remote_amqp_url, remote_queue_name

    # Create a connection to the remote AMQP server using the configuration
    remote_connection_parameters = pika.URLParameters(remote_amqp_url)
    remote_connection = pika.BlockingConnection(remote_connection_parameters)
    remote_channel = remote_connection.channel()

    # Publish the received message to the remote queue
    remote_channel.basic_publish(
        exchange='',
        routing_key=remote_queue_name,
        body=_message
    )

    # Close the connection to the remote AMQP server
    remote_connection.close()


def messageProcessing():
    """
    Recive message from local RabbitMQ server, then:
    1. Re-format it, then publish it to CloudAMQP
    2. Get timestamp, search for image and video with that timestamp, if found, send the image and video to Cloud Storage
    """

    # Define the local AMQP server connection parameters
    local_connection_parameters = pika.ConnectionParameters(
        host='192.168.0.201',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('admin', 'admin')
    )

    # Create a connection to the local AMQP server
    local_connection = pika.BlockingConnection(local_connection_parameters)
    local_channel = local_connection.channel()

    # Declare the queue to receive messages from
    local_queue_name = 'message'
    local_channel.queue_declare(queue=local_queue_name, durable=True)

    # Define a callback function to process received messages
    def local_callback(ch, method, properties, body):
        image_upload_res, video_upload_res = sendImageAndVideo(body)
        if image_upload_res:
        # print(f"{cloudMessageGenerate(body)}\n")
            sendMessage(cloudMessageGenerate(body))
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
    if (not envFileParser() or not configFileParser()):
        print(f'Error while parsing .env or message_config.txt file', file=sys.stderr)
        sys.exit(1)

    messageProcessing()
