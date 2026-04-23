# This will generate greeting message for Aura OS

from datetime import datetime
from activity_tracker import get_power_status , get_network_status , get_security_status
from pattern_engine import get_top_app_per_hour
from productivity_engine import get_productivity_report
from prediction_engine import get_predictions

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

report = get_productivity_report()
prediction = get_predictions()

# This will give the perfect greeting message
def get_greeting():
    greeting_time = get_greeting_time()
    power = get_power_status()
    network = get_network_status()
    top_app  = get_top_app_per_hour()
    security = get_security_status()
    current_hour = datetime.now().hour

    battery_info = str(power['Percent']) + ' %'
    if power['Plugged in']:
        battery_info += ' Charging'

    next_app = prediction['next_app']
    if next_app:
        next_app_line = f"You will likely open {prediction['next_app'].replace('exe', '')} soon"
    else :
        next_app_line = "No specific app predicted for this hour"

    # message = greeting_time + '\nBattery : ' + battery_info + '\nConnected to : ' + network['Wi-Fi']['name'] + ' ' + network['Wi-Fi']['signal'] + '\nYou usually use ' + top_app.get(current_hour , 'nothing specific') + ' at this hour' + '\nDefender is ' + ('Active' if security['Defender']['status'] else 'Inactive') + '\nTotal Session :' + str(report["total_session"]) + '\nAverage Work Duration :' + str(report["avg_duration"]) + '\nMost Productive Day :' + report["most_productive_day"] + '\nPeak working hours :' + str(report["peak_hours"])

    message = f"""
{greeting_time}
Battery : {battery_info} - draining at {prediction['battery_drain']} % per hour
Connected to : {network['Wi-Fi']['name']} {network['Wi-Fi']['signal']}
{next_app_line}
Defender is {('Active' if security['Defender']['status'] else 'Inactive')}
Total Sessions till now is {str(report['total_session'])} and your most productive day is {report['most_productive_day']} and your peak working hours are {', '.join([h[0] + ':00' for h in report['peak_hours']])}
You usually wrap up around {prediction['session_end']}:00
Average session duration is {round(report['avg_duration'] / 60 , 1)} hrs
"""

    return message