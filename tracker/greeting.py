from datetime import datetime
from activity_tracker import get_power_status , get_network_status , get_security_status
from pattern_engine import get_top_app_per_hour

# This will give the greeting according to the time
def get_greeting_time():
    current_hour = datetime.now().hour
    if current_hour > 5 and current_hour < 12:
        return 'Good Morning!'
    elif current_hour >= 12 and current_hour < 17:
        return 'Good Afternoon!'
    elif current_hour >= 17 and current_hour < 21:
        return 'Good Evening!'
    else:
        return 'Good Night!'

# This will give the perfect greeting message
def get_greeting():
    greeting_time = get_greeting_time()
    power = get_power_status()
    network = get_network_status()
    top_app  = get_top_app_per_hour()
    security = get_security_status()
    current_hour = datetime.now().hour

    message = greeting_time + '\nBattery : ' + str(power['Percent']) + ' %' + '\nConnected to : ' + network['Wi-Fi']['name'] + ' ' + network['Wi-Fi']['signal'] + '\nYou usually use ' + top_app.get(current_hour , 'nothing specific') + ' at this hour' + '\nDefender is ' + ('Active' if security['Defender']['status'] else 'Inactive')

    return message