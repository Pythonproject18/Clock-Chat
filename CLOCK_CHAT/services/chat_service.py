from datetime import datetime, timedelta
import pytz

def global_timestamp(timestamp):
    # Get current time in the same timezone as timestamp
    now = datetime.now(timestamp.tzinfo)

    diff = now - timestamp

    if diff < timedelta(days=1) and now.date() == timestamp.date():
        return f"Today at {timestamp.strftime('%I:%M %p')}"
    elif diff < timedelta(days=2) and (now.date() - timestamp.date()).days == 1:
        return f"Yesterday at {timestamp.strftime('%I:%M %p')}"
    elif diff < timedelta(days=7):
        return f"{timestamp.strftime('%A')} at {timestamp.strftime('%I:%M %p')}"
    else:
        return timestamp.strftime('%d-%m-%Y')
