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
                    temperature_air REAL,
                    humidity_air REAL
                )''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('river_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO sensor_data (
    timestamp, latitude, longitude, ph, turbidity,
    temperature_water, tds, temperature_air, humidity_air)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    (
        datetime.now().isoformat(),
        float(data['latitude']),
        float(data['longitude']),
        float(data['ph']),
        float(data['turbidity']),
        float(data['temperature_water']),
        float(data['tds']),
        float(data['temperature_air']),
        float(data['humidity_air'])
    ))

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
    c.execute('''SELECT latitude, longitude, timestamp, ph, turbidity, temperature_water, tds, temperature_air, humidity_air
                 FROM sensor_data''')
    coords = c.fetchall()
    conn.close()
    return coords





