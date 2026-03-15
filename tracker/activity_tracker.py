import psutil

ESSENTIAL_SERVICES = ['WlanSvc','Wcmsvc','WwanSvc','Wcncsvc','bthserv','BluetoothUserService','BTAGService','BthAvctpSvc','Audiosrv','AudioEndpointBuilder','MMCSS','MpsSvc','BFE','SharedAccess','WinDefend','WdNisSvc','Sense','SecurityHealthService','wuauserv','UsoSvc','BITS','DoSvc','WaaSMedicSvc','Dhcp','Dnscache','NlaSvc','Netman','Netprofm','iphlpsvc','lmhosts','WinHttpAutoProxySvc','RasMan','RemoteAccess','FrameServer','FrameServerMonitor','Audiosrv','AudioEndpointBuilder','MMCSS','hidserv','DeviceAssociationService','PlugPlay','SharedAccess','icssvc','WlanSvc','Spooler','PrintNotify']
# This gives the list of all process which are not needed my AuraOS
def get_blacklist():
    blacklist = [] 
    for each_process in psutil.process_iter(['name' , 'exe']):
        if each_process.info['exe'] is None:
            blacklist.append(each_process.info['name'])
        if each_process.info['exe'] is not None and ':\\' in each_process.info['exe']:
            if 'Windows\\System32' in each_process.info['exe']:
                blacklist.append(each_process.info['name'])
            if each_process.info['exe'].endswith('.tmp'):
                blacklist.append(each_process.info['name'])
    return blacklist 

# This give the list of all process which are required by AuraOS
def get_running_apps():
    apps = [] 
    blacklist = get_blacklist()
    for each_process in psutil.process_iter(['name' , 'exe']):
        if each_process.info['exe'] is not None and ':\\' in each_process.info['exe']:
            if 'Windows\\System32' not in each_process.info['exe']:
                if len(each_process.info['name']) < 35:
                    if each_process.info['name'] not in blacklist:
                        apps.append(each_process.info['name'])
    return set(apps)

# This gives the list of all essential windows services which are running 
def get_essential_services():
    services =[]
    for service in psutil.win_service_iter():
        if service.name() in ESSENTIAL_SERVICES and service.status() == 'running':
            services.append(service.name())
    return set(services)
