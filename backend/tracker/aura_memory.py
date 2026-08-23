import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR , 'aura_memory.db')

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS sessions(
                   id INTEGER PRIMARY KEY AUTOINCREMENT ,
                   login_time TEXT ,
                   wifi_name TEXT ,
                   battery INTEGER ,
                   logout_time TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS snapshots(
                   id INTEGER PRIMARY KEY AUTOINCREMENT ,
                   session_id INTEGER,
                   time_stamp TEXT,
                   active_apps TEXT,
                   battery INTEGER,
                   cpu_usage INTEGER,
                   ram_usage INTEGER,
                   wifi_signal INTEGER)""")
    
    conn.commit()
    conn.close()

def save_sessions(login_time , wifi_name , battery):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO sessions (login_time , wifi_name , battery)
                   VALUES(? ,? ,?)""",(login_time , wifi_name , battery))
    i = cursor.lastrowid
    conn.commit()
    conn.close()
    return i 

def save_snapshots(session_id , time_stamp , active_apps , battery , cpu_usage , ram_usage , wifi_signal):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO snapshots (session_id , time_stamp ,
                   active_apps , battery , cpu_usage , ram_usage , wifi_signal) VALUES (? ,? ,? ,? ,? ,? ,?)""" ,
                   (session_id , time_stamp , str(active_apps) , battery , cpu_usage , ram_usage , wifi_signal))
    conn.commit()
    conn.close()

def update_logout(session_id , logout_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE sessions SET logout_time = ? WHERE id = ?""",(logout_time , session_id))
    conn.commit()
    conn.close()

def get_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    data = cursor.fetchall()
    conn.close()
    return data