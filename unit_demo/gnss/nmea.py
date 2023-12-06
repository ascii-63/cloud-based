import serial
import pynmea2


def process_nmea_message(message):
    try:
        # Parse the NMEA sentence
        nmea_object = pynmea2.parse(message)

        # Print message information
        if isinstance(nmea_object, pynmea2.GGA):
            print(
                f'Catch GGA message:\n \tLatitude: {nmea_object.latitude}, Longitude: {nmea_object.longitude}')

        elif isinstance(nmea_object, pynmea2.RMC):
            print(
                f'Catch RMC message:')

        elif isinstance(nmea_object, pynmea2.GSA):
            print(
                f'Catch GSA message:')

        elif isinstance(nmea_object, pynmea2.GSV):
            print(
                f'Catch GSV message:'
            )
        elif isinstance(nmea_object, pynmea2.GLL):
            print(
                f'Catch GLL message:'
            )

    except pynmea2.ParseError as e:
        # print(f'Error parsing NMEA sentence: {e}')
        pass


if __name__ == "__main__":
    port_name = '/dev/ttyACM0'
    baud_rate = 9600

    ser = serial.Serial(port_name, baudrate=baud_rate, timeout=1)

    try:
        while True:
            # data = ser.readline().decode('utf-8')
            data = ser.readline().decode('utf-8', errors='replace')
            # print(data, end='')  # Print the raw NMEA sentence
            process_nmea_message(data)
    except KeyboardInterrupt:
        ser.close()
