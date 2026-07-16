import json
import sqlite3
import geoip2.database

reader = geoip2.database.Reader("GeoLite2-City.mmdb")

conn = sqlite3.connect("iot_attacks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    country TEXT,
    username TEXT,
    password TEXT,
    command TEXT,
    timestamp TEXT
)
""")

log_file = "../cowrie/var/log/cowrie/cowrie.json"

with open(log_file, "r") as f:
    for line in f:
        try:
            data = json.loads(line)

            ip = data.get("src_ip")
            username = data.get("username")
            password = data.get("password")
            command = data.get("input")
            timestamp = data.get("timestamp")

            country = "Unknown"

            if ip:
                try:
                    response = reader.city(ip)
                    country = response.country.name
                except:
                    country = "Local / Private Network"

                cursor.execute("""
                    INSERT INTO attacks (ip, country, username, password, command, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (ip, country, username, password, command, timestamp))

        except:
            pass

conn.commit()
conn.close()

print("Geo-enhanced logs saved")

