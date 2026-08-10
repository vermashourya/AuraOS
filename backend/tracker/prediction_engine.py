# This will help the AuraOS to predict the system stats

import os
import sqlite3
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'aura_memory.db')

# This will predict when the battery will drain according to usage pattern
def predict_battery_drain():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    snapshot = cursor.execute('''SELECT battery, time_stamp FROM snapshots''').fetchall()
    conn.close()

    total_drain = 0 
    total_time = 0
    for i in range(1 , len(snapshot)):
        prev_battery, prev_time = snapshot[i-1]
        curr_battery, curr_time = snapshot[i]
        t1 = datetime.strptime(prev_time, "%a %b %d %H:%M:%S %Y")
        t2 = datetime.strptime(curr_time, "%a %b %d %H:%M:%S %Y")
        if curr_battery < prev_battery:
            total_drain += (prev_battery - curr_battery)
            total_time += (t2 - t1).total_seconds() 
    
    if total_time == 0 :
        return 0
    
    avg_drain = total_drain / (total_time / 3600)

    return (round(avg_drain, 2))

# This will predict that what app will be used next
def predict_next_app():
    conn= sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    snapshot = cursor.execute('''SELECT active_apps, time_stamp FROM snapshots''').fetchall()
    conn.close()

    curr_time = datetime.now().strftime("%H")
    for data in snapshot:
        app_str, time_str = data 
        app_str = app_str.strip("{}")
        apps = [app.strip().strip("'") for app in app_str.split(",")]
        time = time_str.split()[3].split(":")[0]
        
        if time == curr_time:
            return Counter(apps).most_common(1)[0][0]
        else:
            None
        
# This will predict when you are going to close your system
def predict_session_end():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    session = cursor.execute('''SELECT logout_time FROM sessions WHERE logout_time IS NOT NULL''').fetchall()
    conn.close()

    logout = []
    for time in session:
        time_str = time[0]
        hour = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y").hour
        logout.append(hour)
    
    if not logout:
        return 'Unknown'

    return Counter(logout).most_common(1)[0][0]

# This will combine all predictions into one
def get_predictions():
    return dict({
        'battery_drain': predict_battery_drain(),
        'next_app': predict_next_app(),
        'session_end': predict_session_end()
    })
