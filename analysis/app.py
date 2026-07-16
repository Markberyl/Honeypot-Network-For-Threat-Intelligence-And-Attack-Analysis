from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("attacks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attacks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT ip, COUNT(*) FROM attacks GROUP BY ip ORDER BY COUNT(*) DESC LIMIT 5")
    top_ips = cursor.fetchall()

    return f"""
    <h1>IoT Honeypot Dashboard</h1>
    <p>Total Attacks: {total}</p>
    <h3>Top Attackers:</h3>
    <p>{top_ips}</p>
    """

app.run(host="0.0.0.0", port=5000)
