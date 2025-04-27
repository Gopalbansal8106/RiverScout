import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('river_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    latitude REAL,
                    longitude REAL,
                    ph REAL,
                    turbidity REAL,
                    temperature_water REAL,
                    tds REAL,
                    gas REAL,
                    temperature_air REAL,
                    humidity_air REAL
                )''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('river_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO sensor_data (timestamp, latitude, longitude, ph, turbidity, temperature_water, tds, gas, temperature_air, humidity_air)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(), data['latitude'], data['longitude'], data['ph'],
               data['turbidity'], data['temperature_water'], data['tds'],
               data['gas'], data['temperature_air'], data['humidity_air']))
    conn.commit()
    conn.close()

def fetch_all_data():
    conn = sqlite3.connect('river_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM sensor_data')
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_map_data():
    conn = sqlite3.connect('river_data.db')
    c = conn.cursor()
    c.execute('''SELECT latitude, longitude, timestamp, temperature_water, ph, turbidity, gas 
                 FROM sensor_data''')
    coords = c.fetchall()
    conn.close()
    return coords



