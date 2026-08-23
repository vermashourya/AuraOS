import os
import sqlite3
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'aura_memory.db')


def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    session = cursor.execute('''SELECT * FROM sessions WHERE logout_time IS NOT NULL''').fetchall()
    conn.close()
    
    return session


def get_session_duration(login_time, logout_time):
    login = datetime.strptime(login_time, "%d %b %Y %H:%M")
    logout = datetime.strptime(logout_time, "%a %b %d %H:%M:%S %Y")
    duration = logout - login 

    return duration.total_seconds() / 60


def get_average_session_duration():
    sessions = get_all_sessions()
    avg = []
    for session in sessions:
        avg.append(get_session_duration(session[1], session[4]))

    if not avg:
        return 0

    return round((sum(avg) / len(avg)), 2)


def get_most_productive_day():
    sessions = get_all_sessions()
    days_total = Counter()
    for session in sessions:
        login = datetime.strptime(session[1], "%d %b %Y %H:%M")
        duration = get_session_duration(session[1], session[4])
        day = login.weekday()
        days_total[day] += duration
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if not days_total:
        return 'No data Yet'
    
    return days[days_total.most_common(1)[0][0]]


def get_peak_hours():
    sessions = get_all_sessions()
    hours = []
    for session in sessions:
        hour = datetime.strftime(datetime.strptime(session[1], "%d %b %Y %H:%M"), "%H")
        hours.append(hour)
    
    peak = Counter(hours)
    return peak.most_common(3)


def get_total_session():
    sessions = get_all_sessions()
    return len(sessions)


def get_productivity_report():
    report = {
        "total_session" : get_total_session(),
        "avg_duration" : get_average_session_duration(),
        "most_productive_day" : get_most_productive_day(),
        "peak_hours" : get_peak_hours()
    }

    return report