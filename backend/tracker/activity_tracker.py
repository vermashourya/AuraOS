# ACTIVITY TRACKER of AURA-OS
# This unit tells the AURA-OS about all the activity of the system

import os
import psutil
import subprocess
import wmi
import time
from datetime import datetime
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL

# This is the list of all the essential services of windows
ESSENTIAL_SERVICES = ['WlanSvc','Wcmsvc','WwanSvc','Wcncsvc','bthserv','BluetoothUserService','BTAGService','BthAvctpSvc','Audiosrv','AudioEndpointBuilder','MMCSS','MpsSvc','BFE','SharedAccess','WinDefend','WdNisSvc','Sense','SecurityHealthService','wuauserv','UsoSvc','BITS','DoSvc','WaaSMedicSvc','Dhcp','Dnscache','NlaSvc','Netman','Netprofm','iphlpsvc','lmhosts','WinHttpAutoProxySvc','RasMan','RemoteAccess','FrameServer','FrameServerMonitor','Audiosrv','AudioEndpointBuilder','MMCSS','hidserv','DeviceAssociationService','PlugPlay','SharedAccess','icssvc','WlanSvc','Spooler','PrintNotify']

# This will dynamically give the system drive name
windows_drive = os.environ.get('SystemDrive' , 'C:') + '\\'

# This give the list of all processes which are required by AuraOS
def get_running_apps():
    apps = [] 
    w = wmi.WMI()
    for process in w.Win32_Process():
            if process.ExecutablePath is not None:
                if 'WindowsApps\\Microsoft.' not in process.ExecutablePath:
                    if windows_drive + 'Users' in process.ExecutablePath or windows_drive + 'Program Files' in process.ExecutablePath:
                        if len(process.Name) < 35:
                            apps.append(process.Name)

    return set(apps)

# This gives the list of all essential windows services which are running 
def get_essential_services():
    services =[]
    for service in psutil.win_service_iter():
        if service.name() in ESSENTIAL_SERVICES and service.status() == 'running':
            services.append(service.name())

    return set(services)

# This gives the status of networks connected
def get_network_status():
    network = dict({})

    for iface , stat in psutil.net_if_stats().items():
        if 'Bluetooth' in iface:
            network['Bluetooth'] = {'status':stat.isup , 'speed':stat.speed}
        if 'Local Area Connection' in iface:
            network['Ethernet'] = {'status':stat.isup , 'speed':stat.speed}
        elif 'Ethernet' in iface:
            network['Ethernet'] = {'status':stat.isup , 'speed':stat.speed}
    try:
        result = subprocess.check_output(['netsh','wlan','show','interfaces'] , text = True)
        for line in result.split("\n"):
            if 'SSID' in line and not 'BSSID' in line:
                network.setdefault('Wi-Fi' , {}).update({'name':line.split(":")[1].strip()})
            if 'State' in line:
                network.setdefault('Wi-Fi' , {}).update({'status':line.split(":")[1].strip()})
            if 'Receive rate' in line:
                network.setdefault('Wi-Fi' , {}).update({'speed':line.split(":")[1].strip() + ' Mbps'})
            if 'Signal' in line:            
                network.setdefault('Wi-Fi' , {}).update({'signal':line.split(":")[1].strip()})
    except subprocess.CalledProcessError:
        network['Wi-Fi'] = {'status':'disconnected', 'name':None, 'speed':'0 Mbps', 'signal':'0 %'}
    
    return network   

# This is a helper function for get_security_status() that convert the date and time from the wmi into user readable format
def parse_wmi_date(date):
    if not isinstance(date , str):
        return 'Never'
    else:
        clean_date = datetime.strptime(date[:14] , "%Y%m%d%H%M%S")
        return clean_date.strftime("%d %b %Y %H:%M")
    
# This is a helper function for get_security_status() that gives the age of scans in correct format
def parse_wmi_age(age):
    if age is None or age == 4294967295 or age == -1:
        return 'Never'
    elif age == 0:
        return 'Today'
    else:
        return str(age) + ' days ago'

# This is a helper function for get_security_status() that convertes the firewall status
def firewall_status(fire):
    if fire == 1:
        return 'On'
    else:
        return 'Off'

# This gives the firewall and defender status
def get_security_status():
    security = dict({})
    w = wmi.WMI(namespace = 'root/microsoft/windows/defender')
    for item in w.MSFT_MpComputerStatus():
        security['Defender'] = {'status':item.AntivirusEnabled , 'protection status':item.RealTimeProtectionEnabled , 'out of date':getattr(item , 'DefenderSignaturesOutOfDate' , None) , 'last quick scan time':parse_wmi_date(item.QuickScanEndTime) , 'quick scan overdue':item.QuickScanOverdue , 'last quick scan':parse_wmi_age(getattr(item ,'QuickScanAge' , None)) , 'last full scan time':parse_wmi_date(item.FullScanEndTime) , 'full scan overdue':item.FullScanOverdue , 'last full scan':parse_wmi_age(getattr(item, 'FullScanAge' , None)) , 'reboot required':getattr(item , 'RebootRequired' , None)}

    w2 = wmi.WMI(namespace = 'root/standardcimv2')
    for item in w2.MSFT_NetFirewallProfile():
        security.setdefault('Firewall' , {}).update({item.Name:firewall_status(item.Enabled)})
    
    return security

# This gives the audio status 
def get_audio_status():
    audio = dict({})
    try:
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        audio['Volume'] = int(volume.GetMasterVolumeLevelScalar() * 100)
        audio['Mute'] = volume.GetMute() == 1
        audio['Device'] = device.FriendlyName
        sessions = AudioUtilities.GetAllSessions()
        audio['Audio by'] = []
        for session in sessions:
            if session.Process and session.State == 1:
                audio['Audio by'].append(session.Process.name())

        return audio    
    except:
        return {'Volume' : None , 'Mute' : None , 'Device' : 'No Audio Device'}

# This gives the power status
def get_power_status():
    power = dict({})
    battery = psutil.sensors_battery()
    
    if battery is None:
        return {'Percent' : None , 'Time Left' : None , 'Plugged in' : True}
    
    power['Percent'] = battery.percent 
    # power['Time Left'] = str(round(battery.secsleft / (60 * 60 * 60))) + ' mins'
    if battery.power_plugged:
        power['Time Left'] = '~'
    elif battery.secsleft == -1 or battery.secsleft > 86400:
        power['Time Left'] = 'Calculating...'
    else:
        sec = battery.secsleft
        power['Time Left'] = str(time.strftime("%H:%M", time.gmtime(sec))) + ' hrs'
    power['Plugged in'] = battery.power_plugged

    return power

# This gives the hardware status
def get_hardware_status():
    hardware = dict({})
    hardware['CPU'] = {'Usage':psutil.cpu_percent(interval=1) , 'Cores':psutil.cpu_count()}
    hardware['RAM'] = {'Usage':psutil.virtual_memory().percent , 'Available':str(round(psutil.virtual_memory().available / (1024 ** 3) , 1)) + ' GB' , 'Total':str(round(psutil.virtual_memory().total / (1024 ** 3) , 1)) + ' GB'}
    hardware['Disk'] = {'Usage':psutil.disk_usage(windows_drive).percent , 'Available':str(round(psutil.disk_usage(windows_drive).free / (1024 ** 3) , 1)) + ' GB' , 'Total':str(round(psutil.disk_usage(windows_drive).total / (1024 ** 3) , 1)) + ' GB'}
    w = wmi.WMI()
    hardware['GPU'] = []
    for gpu in w.Win32_VideoController():
        hardware['GPU'].append({'Name':gpu.Name , 'VRAM':str(round(gpu.AdapterRAM / (1024 ** 3) , 1)) + ' GB'})

    return hardware