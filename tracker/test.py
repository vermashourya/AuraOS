import psutil
import pywifi
import subprocess
import wmi
from pycaw.pycaw import AudioUtilities 
import sqlite3
from aura_memory import save_sessions

# # filtered_network = []
# # iface = psutil.net_if_stats()
# # for name , stats in iface.items():
# #     if 'Wi-Fi'in name:
# #         network['Wi-Fi'] = {'status':stats.isup , 'speed':stats.speed}
# #     if 'Bluetooth Network Connection' in name:
# #         network['Bluetooth'] = {'status':stats.isup , 'speed':stats.speed}
# #     if 'Local Area Connection' in name:
# #         network['Ethernet'] = {'status':stats.isup , 'speed':stats.speed}
# # wifi = pywifi.PyWiFi()
# # iface = wifi.interfaces()[0]
# # iface.scan()
# # time.sleep(2)
# # results = iface.scan_results
# # result_map = {r.ssid : r for r in results}
# # profiles = iface.network_profiles()
# # for profile in profiles:
# #     if profile.ssid in result_map:
# #         filtered_network.append(result_map[profile.ssid])
# # strongest_profile = max(filtered_network , key = lambda r : r.signal)
# # for profile in profiles:
# #     if profile.ssid in result_map:
# #         network['Wi-Fi'].update({'name':strongest_profile.ssid , 'signal':strongest_profile.signal})
# #         break 

# def get_network_status():
#     network = dict({})
#     for name , stats in psutil.net_if_stats().items():
#         if name == 'Wi-Fi':
#             network['Wi-Fi'] = {'speed':stats.speed , 'status':stats.isup , 'name':name}
#     return network

# # print(get_network_status())

# stat = psutil.net_if_stats()
# print(repr(stat)) 

# wifi = pywifi.PyWiFi()
# iface = wifi.interfaces()[0]
# print(dir(iface))

# profiles = iface.network_profiles()
# for profile in profiles:
#     print(profile.ssid, dir(profile))

# def get_network_status():
#     network = dict({})
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0]

#     if iface.status() == 4:
#         profiles = iface.network_profiles()
#         for profile in profiles:
#             network['Wi-Fi'] = {'Name':profile.ssid}
#     return network

# print(get_network_status())

# import time 
# wifi = pywifi.PyWiFi()
# iface = wifi.interfaces()[0]    
# iface.scan()
# time.sleep(2)
# results = iface.scan_results()
# result_map = {r.ssid : r for r in results}
# profiles = iface.network_profiles()
# strongest = max(results , key=lambda r: r.signal)
# for profile in profiles:
#     if profile.ssid in result_map:
#         print(strongest.ssid)

# result = subprocess.check_output(['netsh','wlan','show','interfaces'] ,text=True)
# for line in result.split("\n"):
#     if 'SSID' in line and not 'BSSID' in line:
#         print(line.split(":")[1].strip())
#     if 'State' in line:
#         print(line.split(":")[1].strip())
#     if 'Receive rate' in line:
#         print(line.split(":")[1].strip())
#     if 'Signal' in line:
#         print(line.split(":")[1].strip())

# w = wmi.WMI()
# for item in w.Win32_Service(Name = 'WinDefend'):
#     print(item.state)
#     print(item.status)
#     print(item.started)
# w2 = wmi.WMI(namespace = 'root/microsoft/windows/defender')
# for item in w2.MSFT_MpComputerStatus():
#     print(getattr(item, 'DefenderSignaturesOutOfDate', None))
# from datetime import datetime

# wmi_date = "20260315144152.196000+000"
# clean_date = datetime.strptime(wmi_date[:14], "%Y%m%d%H%M%S")
# print(clean_date.strftime("%d %b %Y %I:%M %p"))
# time = "20260315144152.196000+000"

# def parse_wmi_dates(time):
#     if not isinstance(time,str):
#         return 'Never'
#     else:        
#         clean_date = datetime.strptime(time[:14], "%Y%m%d%H%M%S")
#         return clean_date.strftime("%d %b %Y %H:%M")

# print(parse_wmi_dates(time))

# w = wmi.WMI(namespace = 'root/standardcimv2')
# for item in w.MSFT_NetFirewallProfile():
#     print(item.name , item.enabled)

# sessions = AudioUtilities.GetAllSessions()
# for session in sessions:
#     if session.Process:
#         print(session.Process.name() , session.State)

# print(psutil.sensors_battery())

# w = wmi.WMI()
# for gpu in w.Win32_VideoController():
#     print(gpu.Name, gpu.AdapterRAM)

# print(psutil.virtual_memory().percent)
# print(psutil.virtual_memory().available / (1024 * 1024 * 1024))
# print(psutil.virtual_memory().percent)

# conn = sqlite3.connect('test.db')
# print("Connected")
# conn.close()
# print("Closed!")

from aura_memory import get_sessions
print(get_sessions())