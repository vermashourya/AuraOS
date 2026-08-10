# This will give notification to user whenever any wrong happen

import os
import sqlite3
from datetime import datetime
from plyer import notification
from tracker.activity_tracker import get_power_status , get_security_status , get_hardware_status , get_network_status
from tracker.prediction_engine import predict_battery_drain

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'aura_memory.db')

# This will give notification to user when battery goes low
def check_battery():
    battery = get_power_status()
    if battery is not None:
        if battery['Percent'] < 10 and not battery['Plugged in']:
            notification.notify(title = 'Aura OS' , message = 'Critical Battery! Save your work and plug in charger' , timeout = 10)
        elif battery['Percent'] < 20 and not battery['Plugged in']:
            notification.notify(title = 'Aura OS' , message = 'Battery Low! Plug in your charger' , timeout = 10)

# This will give notification to user if defender is off
def check_defender():
    security = get_security_status()
    if not security['Defender']['status']:
        notification.notify(title = 'Aura OS' , message = 'Warning: Antivirus is disabled' , timeout = 10)
    if not security['Defender']['protection status']:
        notification.notify(title = 'Aura OS' , message = 'Warning: Real time protection is off' , timeout = 10)

# This will give notification to user if system resource hit peak
def check_hardware():
    hardware = get_hardware_status()
    if hardware['CPU']['Usage'] > 90:
        notification.notify(title = 'Aura OS' , message = 'CPU Overload' , timeout = 10)
    if hardware['RAM']['Usage'] > 90:
        notification.notify(title = 'Aura OS' , message = 'RAM almost full' , timeout = 10)
    if hardware['Disk']['Usage'] > 90:
        notification.notify(title = 'Aura OS' , message = 'Disk almost full' , timeout = 10)

# This will give notification to user if wifi signal got weak
def check_wifi():
    network = get_network_status()
    if network.get('Wi-Fi' , {}).get('status') == 'connected':
        signal = int(network['Wi-Fi']['signal'].replace('%' , ''))
        if signal < 30:
            notification.notify(title = 'Aura OS' , message = 'Weak Wi-Fi signal' , timeout = 10)

# This will check and notify if battery is draining faster than usual
def check_battery_drain():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    snapshot = cursor.execute('''SELECT battery, time_stamp FROM snapshots WHERE time_stamp >= datetime('now', '-1 hour')''').fetchall()
    conn.close()

    total_time = 0 
    total_drain = 0 
    
    if len(snapshot) < 2:
        return 
    
    for i in range(1, len(snapshot)):
        prev_battery, prev_time = snapshot[i-1]
        curr_battery, curr_time = snapshot[i]
        t1 = datetime.strptime(prev_time, "%a %b %d %H:%M:%S %Y")
        t2 = datetime.strptime(curr_time, "%a %b %d %H:%M:%S %Y")
        if curr_battery < prev_battery:
            total_drain += (prev_battery - curr_battery)
            total_time += (t2 -t1).total_seconds()
    
    if total_time == 0 :
        return 
    
    actual_drain = round((total_drain / (total_time / 3600)), 2)
    predict_drain = predict_battery_drain()
    
    if actual_drain > predict_drain * 2:
        notification.notify(title= 'Aura OS', message= 'Unusual Battery Drain', timeout= 10)

# This will check and notify sudden cpu spike
def check_cpu_spike():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    snapshot = cursor.execute('''SELECT cpu_usage FROM snapshots''').fetchall()
    conn.close()

    sum = 0 
    i = 0 

    if len(snapshot) == 0 :
        return
    
    for cpu in snapshot:
        sum += cpu[0]
        i = i + 1

    avg_CPU = sum / i
    curr_CPU = get_hardware_status()['CPU']['Usage']

    if curr_CPU > avg_CPU * 2 and curr_CPU > 80:
        notification.notify(title= 'Aura OS', message= 'Unusual CPU Spike', timeout= 10)

# This will invoke and check all functions
def run_checks():
    check_battery()
    check_defender()
    check_hardware()
    check_wifi()
    check_battery_drain()
    check_cpu_spike()