# This will give notification to user whenever any wrong happen

from plyer import notification
from activity_tracker import get_power_status , get_security_status , get_hardware_status , get_network_status

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

# This will invoke and check all functions
def run_checks():
    check_battery()
    check_defender()
    check_hardware()
    check_wifi()