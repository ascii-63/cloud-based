import serial
import pynmea2

import sys

def getLatLonFromNMEAMessage(_message):
    """Get Latitude and Longitude from NMEA2 message"""
    try: 
        # Parse the NMEA sentence
        nmea_object = pynmea2.parse(_message)

        if isinstance(nmea_object, pynmea2.GGA):
            lat = nmea_object.latitude
            lon = nmea_object.longitude
            return lat, lon
    except pynmea2.ParseError as e:
        return 0, 0
    
    return 0, 0


if __name__ == "__main__":
    port_name = '/dev/ttyACM0'
    baud_rate = 9600

    if (len(sys.argv) == 3):
        port_name = sys.argv[1]
        baud_rate = sys.argv[2]
        print(f'Get port name ({port_name}) and baud rate ({baud_rate}) from arguments.')
    
    ser = serial.Serial(port_name, baudrate=baud_rate, timeout=1)

    try:
        while True:
            data = ser.readline().decode('utf-8', errors='replace')
            # print(data, end='')  # Print the raw NMEA sentence

            lat, lon = getLatLonFromNMEAMessage(data)
            if (lat != 0 and lon != 0):
                print(f'Lat: {lat}, Lon: {lon}')
    except KeyboardInterrupt:
        ser.close()