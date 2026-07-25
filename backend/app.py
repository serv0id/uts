import base64
import sqlite3
from typing import Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from flask import Flask, request, jsonify
from flask_cors import CORS

import config

app = Flask(__name__)
# CORS(app, origins=["https://uts.desrever.dev"])


@app.route('/uts/stations', methods=['GET'])
def search_stations():
    query = request.args.get('q', '').upper()
    with sqlite3.connect("dec.db") as con:
        cur = con.cursor()
        res = cur.execute("""
            SELECT STATION_CODE, STATION_NAME 
            FROM MUSER_STATION 
            WHERE STATION_NAME LIKE ? OR STATION_CODE LIKE ?
            LIMIT 20
        """, (f"%{query}%", f"%{query}%"))
        return jsonify(res.fetchall())


@app.route('/uts/coordinates/<scd>', methods=['GET'])
def get_cor(scd) -> dict:
    with sqlite3.connect("dec.db") as con:
        cur = con.cursor()

        res = cur.execute("SELECT Latitude,Longitude FROM MUSER_STATION WHERE STATION_CODE=?", (scd,))
        coords = res.fetchone()

        return {"lat": coords[0], "lon": coords[1]}


@app.route('/uts/encrypt', methods=['POST'])
def encrypt() -> str:
    cipher = AES.new(config.ENCRYPTION_KEY, mode=AES.MODE_ECB)

    ciphertext = cipher.encrypt(pad(request.data, 16))

    return base64.b64encode(ciphertext).decode()
