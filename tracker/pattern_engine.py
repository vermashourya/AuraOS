# By this Aura-OS learns the users working life pattern

import ast 
import os
import sqlite3
from collections import Counter
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR , 'aura_memory.db')

# This will read active apps from database
def get_snapshots():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT active_apps , time_stamp FROM snapshots")
    data = cursor.fetchall()
    apps = []
    for row in data :
        apps.append({
            'apps' : ast.literal_eval(row[0]) , 
            'time' : row[1]
        })
    
    conn.close()
    return apps    

# This will give the most used apps
def get_most_used_apps():
    snapshots = get_snapshots()
    all_apps = [] 
    for app in snapshots:
        for one in app['apps']:
            all_apps.append(one)
    count = Counter(all_apps)

    return count.most_common(5)

# This will give the apps according to time
def get_apps_by_hour():
    snapshots = get_snapshots()
    hourly_apps = dict({})
    for snapshot in snapshots:
        dt = datetime.strptime(snapshot['time'] , '%a %b %d %H:%M:%S %Y')
        hour = dt.hour
        for app in snapshot['apps']:
            hourly_apps.setdefault(hour , []).append(app)

    return hourly_apps

# This will give the apps mostly used acoording by hours.
def get_top_app_per_hour():
    hourly_apps = get_apps_by_hour()
    top_apps = dict({})
    for key in hourly_apps.keys():
        top = hourly_apps.get(key)
        count = Counter(top)
        top_apps[key] = count.most_common(1)[0][0]
    
    return top_apps