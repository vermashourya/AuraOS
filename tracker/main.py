# MAIN Aura-OS
# This is the heart of Aura-OS - brings everything alive

import time
from datetime import datetime
import wmi
from greeting import get_greeting
from activity_tracker import parse_wmi_date , get_hardware_status , get_network_status , get_power_status , get_running_apps
from aura_memory import create_database , save_sessions , save_snapshots , get_sessions , update_logout

# This will give the network name
def get_network_name(network):
    if network.get('Wi-Fi' , {}).get('status') == 'connected':
        return network['Wi-Fi']['name']
    elif network.get('Ethernet' , {}).get('status'):
        return 'Ethernet'
    elif network.get('Local Area Connection' , {}).get('status'):
        return 'Ethernet'
    else:
        return 'No Network Connection'
    
# This will give the signal strength of connected network
def get_network_signal(network):
    if network.get('Wi-Fi' , {}).get('status') == 'connected':
        return network['Wi-Fi']['signal']
    else:
        return 'N/A'

# This will give the time when the Aura-OS starts
def get_login_time():
    w = wmi.WMI()
    for session in w.Win32_LogonSession():
        if session.LogonType == 2:
            return parse_wmi_date(session.StartTime)
        
# This will start the Aura-OS and return session-id
def start_aura():
    create_database()
    login_time = get_login_time()
    network = get_network_name(get_network_status())
    power = get_power_status()
    session_id = save_sessions(login_time , network , power['Percent'])
    print((get_greeting()))
    print('aura_os started!')
    return session_id

# This will take snapshot 
def take_snapshot(session_id):
    current_time = time.ctime()
    running_apps = get_running_apps()
    power = get_power_status()
    hardware_status = get_hardware_status()
    network = get_network_signal(get_network_status())
    save_snapshots(session_id , current_time , running_apps , power['Percent'] , hardware_status['CPU']['Usage'] , hardware_status['RAM']['Usage'] , network)
    print('snapshot taken!')

# This will stop Aura-OS and update logout time
def stop_aura(session_id):
    logout_time = time.ctime()
    update_logout(session_id , logout_time)   
    print('aura_os stopped!')

if __name__ == '__main__':
    session_id = start_aura()
    try:
        while True:
            take_snapshot(session_id)
            time.sleep(300)
    except KeyboardInterrupt:
        stop_aura(session_id)       