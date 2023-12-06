# message.py

from enum import Enum
from datetime import datetime
import json


class Enum_EventType(Enum):
    pass


class Enum_SensorType(Enum):
    pass


class Enum_PlaceType(Enum):
    pass


class Object:
    """
    id: string

    bbox: {"topleftx": int, "toplefty": int, "bottomrightx": int, "bottomrighty": int}

    location: {"lat": float, "lon": float, "alt": float}
    """

    def __init__(self, _id, _bbox, _location):
        self.id = _id
        self.bbox = _bbox
        self.location = _location


class Event:
    """
    id: string

    type: @Enum_EventType (string)
    """

    def __init__(self, _id, _type):
        self.id = _id
        self.type = _type


class Sensor:
    """
    id: integer

    type: @Enum_SensorType (string)

    description: string

    location: {"lat": float, "lon": float, "alt": float}
    """

    def __init__(self, _id, _type, _description, _location):
        self.id = _id
        self.type = _type
        self.description = _description
        self.location = _location


class Place:
    """
    id: integer

    name: string

    type: @Enum_PlaceType (string)

    location: {"lat": float, "lon": float, "alt": float}
    """

    def __init__(self, _id, _name, _type, _location):
        self.id = _id
        self.name = _name
        self.type = _type
        self.location = _location


class Message:
    """
    message_id: string

    timestamp: datetime

    place: @Place

    sensor: @Sensor

    object: @Object

    event: @Event
    """

    def __init__(self, _message_id, _timestamp, _place, _sensor, _object, _event, _imageURL, _videoURL):
        self.message_id = _message_id
        self.timestamp = _timestamp
        self.place = _place
        self.sensor = _sensor
        self.object = _object
        self.event = _event
        self.imageURL = _imageURL
        self.videoURL = _videoURL


##############################################


def getTimestampFromMessage(_message):
    """Get the timestamp of the Message"""

    data = json.loads(_message)
    timestamp_str = data.get('@timestamp')
    if timestamp_str:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return timestamp
    else:
        return None
