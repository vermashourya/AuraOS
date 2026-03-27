import psutil
import subprocess
import wmi
from datetime import datetime
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
from ctypes import POINTER , cast
from comtypes import CLSCTX_ALL


ESSENTIAL_SERVICES = ['WlanSvc','Wcmsvc','WwanSvc','Wcncsvc','bthserv','BluetoothUserService','BTAGService','BthAvctpSvc','Audiosrv','AudioEndpointBuilder','MMCSS','MpsSvc','BFE','SharedAccess','WinDefend','WdNisSvc','Sense','SecurityHealthService','wuauserv','UsoSvc','BITS','DoSvc','WaaSMedicSvc','Dhcp','Dnscache','NlaSvc','Netman','Netprofm','iphlpsvc','lmhosts','WinHttpAutoProxySvc','RasMan','RemoteAccess','FrameServer','FrameServerMonitor','Audiosrv','AudioEndpointBuilder','MMCSS','hidserv','DeviceAssociationService','PlugPlay','SharedAccess','icssvc','WlanSvc','Spooler','PrintNotify']

# This gives all the unwanted processes
def get_blacklist():
    blacklist = [] 
    for each_process in psutil.process_iter(['name' , 'exe']):
        if each_process.info['exe'] is None :
            blacklist.append(each_process.info['name'])
        if each_process.info['exe'] is not None and ':\\' in each_process.info['exe'] :
            if 'Windows\\System32' in each_process.info['exe'] :
                blacklist.append(each_process.info['name'])
            if each_process.info['name'].endswith('.tmp') :
                blacklist.append(each_process.info['name'])
    return blacklist

# This gives all the user running processes
def get_running_apps():
    apps = []
    blacklist = get_blacklist()
    for each_process in psutil.process_iter(['name' , 'exe']) :
        if each_process.info['exe'] is not None and ':\\' in each_process.info['exe']:
            if 'Windows\\System32' not in each_process.info['exe']:
                if len(each_process.info['name']) < 35 :
                    if each_process.info['name'] not in blacklist :
                        apps.append(each_process.info['name'])
    return set(apps)

# This gives all the required services
def get_essential_services():
    services = []
    for service in psutil.win_service_iter():
        if service.name() in ESSENTIAL_SERVICES and service.status() == 'running':
            services.append(service.name())
    return set(services)

# This gives the status of network
def get_network_status():
    network = dict({})
    iface = psutil.net_if_stats()

    for name , stats in iface.items():
        if 'Bluetooth Network Connection' in name:
            network['Bluetooth'] = {'status':stats.isup , 'speed':stats.speed}
        if 'Local Area Connection' in name:
            network['Ethernet'] = {'status':stats.isup , 'speed':stats.speed}

    result = subprocess.check_output(['netsh','wlan','show','interfaces'], text = True)
    for line in result.split("\n"):
        if 'SSID' in line and not 'BSSID' in line:
            network.setdefault('Wi-Fi',{}).update({'name':line.split(":")[1].strip()})
        if 'State' in line:
            network.setdefault('Wi-Fi',{}).update({'status':line.split(":")[1].strip()})
        if 'Receive rate' in line:
            network.setdefault('Wi-Fi',{}).update({'speed':line.split(":")[1].strip()+' Mbps'})
        if 'Signal' in line:
            network.setdefault('Wi-Fi',{}).update({'signal':line.split(":")[1].strip()})
    return network

# This gives the status of Windows Defender and Firewall
def parse_wmi_dates(date):
    if not isinstance(date , str):
        return 'Never'
    else:
        clean_date = datetime.strptime(date[:14], "%Y%m%d%H%M%S")
        return clean_date.strftime("%d %b %Y %H:%M") 
    
def firewall(n):
    if n == 1:
        return 'ON'
    else:
        return 'OFF'

def parse_wmi_age(age):
    if age is None or age == 4294967295 or age == -1:
        return 'Never'
    elif age == 0:
        return 'Today'
    else:
        return str(age) + ' days ago'

def get_security_status():
    security = dict({})
    # defender = subprocess.check_output("powershell Get-MpComputerStatus" , text = True , shell = True)
    # for line in defender.split("\n"):
    #     if 'AntivirusEnabled' in line:
    #         security.setdefault('Defender' , {}).update({'status':line.split(":")[1].strip()})
    #     if 'RealTimeProtection' in line:
    #         security.setdefault('Defender' , {}).update({'protection status':line.split(":")[1].strip()})
    #     if 'DefenderSignaturesOutOfDate' in line:
    #         if line.split(":")[1].strip() == 'False':
    #             security.setdefault('Defender' , {}).update({'up to date':True})
    #         else:
    #             security.setdefault('Defender' , {}).update({'up to date':False})
    #     if 'QuickScanEndTime' in line:
    #         security.setdefault('Defender' , {}).update({'last quick scan time':':'.join(line.split(":")[1:]).strip()})
    #     if 'QuickScanOverdue' in line:
    #         security.setdefault('Defender' , {}).update({'quick scan overdue':line.split(":")[1].strip()})
    #     if 'QuickScanAge' in line :
    #         if line.split(":")[1].strip() == '4294967295':
    #             security.setdefault('Defender' , {}).update({'last quick scan since':'never'})
    #         else:
    #             security.setdefault('Defender' , {}).update({'last quick scan since':line.split(":")[1].strip() + ' days'})
    #     if 'FullScanEndTime' in line:
    #         security.setdefault('Defender' , {}).update({'last full scan time':':'.join(line.split(":")[1:]).strip()})
    #     if 'FullScanOverdue' in line:
    #         security.setdefault('Defender' , {}).update({'full scan overdue':line.split(":")[1].strip()})
    #     if 'FullScanAge' in line :
    #         if line.split(":")[1].strip() == '4294967295':
    #             security.setdefault('Defender' , {}).update({'last full scan since':'never'})
    #         else:
    #             security.setdefault('Defender' , {}).update({'last full scan since':line.split(":")[1].strip() + 'days'})
    #     if 'RebootRequired' in line :
    #         security.setdefault('Defender' , {}).update({'reboot required':line.split(":")[1].strip()})

    # firewall = subprocess.check_output("netsh advfirewall show allprofiles" , text = True , shell = True)
    # current_profile = ''
    # for line in firewall.split("\n"):
    #     if 'Domain' in line:
    #         current_profile = 'Domain'
    #     if 'State' in line and current_profile == 'Domain':
    #         security.setdefault('Firewall' , {}).update({current_profile:line.split()[-1].strip()})
    #     if 'Private' in line:
    #         current_profile = 'Private'
    #     if 'State' in line and current_profile == 'Private':
    #         security.setdefault('Firewall' , {}).update({current_profile:line.split()[-1].strip()})
    #     if 'Public' in line:
    #         current_profile = 'Public'
    #     if 'State' in line and current_profile == 'Public':
    #         security.setdefault('Firewall' , {}).update({current_profile:line.split()[-1].strip()})

    w1 = wmi.WMI(namespace = 'root/microsoft/windows/defender')
    for item in w1.MSFT_MpComputerStatus():
        security['Defender'] = {'status':item.AntivirusEnabled , 'protection status':item.RealTimeProtectionEnabled , 'out of date':getattr(item , 'DefenderSignaturesOutOfDate' , None) , 'last quick scan time':parse_wmi_dates(item.QuickScanEndTime) , 'quick scan overdue':item.QuickScanOverdue , 'last quick scan':parse_wmi_age(getattr(item ,'QuickScanAge' , None)) , 'last full scan time':parse_wmi_dates(item.FullScanEndTime) , 'full scan overdue':item.FullScanOverdue , 'last full scan':parse_wmi_age(getattr(item, 'FullScanAge' , None)) , 'reboot required':getattr(item , 'RebootRequired' , None)}
    
    w3 = wmi.WMI(namespace = 'root/standardcimv2')
    for item in w3.MSFT_NetFirewallProfile():
        security.setdefault('Firewall' , {}).update({item.Name:firewall(item.Enabled)})
    
    return security

def get_audio_status():
    audio = dict({})
    device = AudioUtilities.GetSpeakers()
    volume = device.EndpointVolume
    sessions = AudioUtilities.GetAllSessions()
    audio['Volume'] = int(volume.GetMasterVolumeLevelScalar() * 100)
    if volume.GetMute() == 1:
        audio['Mute'] = True
    else:
        audio['Mute'] = False
    audio['Device'] = device.FriendlyName
    audio['Audio by'] = []
    for session in sessions:
        if session.Process and session.State == 1:
            audio['Audio by'].append(session.Process.name())

    return audio   

def get_power_status():
    power = dict({})
    battery = psutil.sensors_battery()
    power['Percent'] = battery.percent
    power['Time Left'] = str(round(battery.secsleft / 60)) + ' mins'
    power['Plugged in'] = battery.power_plugged

    return power
