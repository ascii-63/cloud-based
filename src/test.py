from datetime import datetime, timedelta

def convertUTC0ToUTC7(timestamp):
    """Convert ts str from UTC+0 to UTC+7"""

    dt_utc0 = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    utc0 = timedelta(hours=0)
    utc7 = timedelta(hours=7)
    dt_utc7 = dt_utc0 + (utc7 - utc0)

    timestamp_utc7 = dt_utc7.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    final_timestamp = timestamp_utc7[0:-4] + timestamp_utc7[-1]

    return final_timestamp