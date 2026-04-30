# This will help Aura OS to think according to you activity

import sqlite3
import os
from collections import Counter
from datetime import datetime
from plyer import notification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'aura_memory.db')

# This will get all the login hours from database
def get_login_hours():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT login_time FROM sessions''')
    hrs = cursor.fetchall()
    conn.close()
    hours = []
    for each in hrs:
        hours.append(each[0].split()[-1].split(':')[0])

    return hours 

def is_unusual_login():
    hours = get_login_hours()
    hrs_freq = Counter(hours)
    current_hour = str(datetime.now().strftime("%H"))
    total = len(hours)

    if total < 5:
        return False # not enough data to judge
    if current_hour not in hours :
        return True # never logged in at this hour
    
    percentage = (hrs_freq[current_hour] / total) * 100
    if percentage < 10 :
        return True # very rare hour
    else:
        return False # normal hour

# This will give message according to login hours
def get_anomaly_message():
    current_hour = str(datetime.now().strftime("%I %p"))
    hours = get_login_hours()
    common = Counter(hours).most_common(1)[0][0]

    return f"""You don't usually login at {current_hour}.
                Your typical login time is around {common}:00.
                Is everything okay?"""

# combines everything and send notification
def check_login_anomaly():
    anomaly = is_unusual_login()
    if anomaly:
        message = get_anomaly_message()
        notification.notify(title = 'Aura OS', message = message, timeout = 10)
        return message
    else:
        return None