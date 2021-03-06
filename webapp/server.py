from flask import Flask, render_template, request, jsonify

import mysql.connector

import os

from datetime import datetime



app = Flask(__name__)

db = mysql.connector.connect(
    host="bengstock.mysql.pythonanywhere-services.com",
    user="bengstock",
    password="tomtimsql",
    database="bengstock$default"
    )


@app.route("/")
def home():

    db.reconnect()
    cur = db.cursor()
    
    cur.execute("select * from data")
    res = cur.fetchall()

    format = "%Y-%m-%d %H.%M"

    x_axis = [datetime.strptime(f"{i[1]} {i[2]}", format).strftime("%H:%M") for i in res]

    y_axis = [i[3] / 100 for i in res]

    daily_max = res[-1][4]
    last_value = res[-1][3]

    return render_template("home.html")


@app.route("/get_data")
def send_data():

    try:
        db.reconnect()
        cur = db.cursor()
        
        cur.execute("select * from data")
        res = cur.fetchall()

        format = "%Y-%m-%d %H.%M"

        x_axis = [datetime.strptime(f"{i[1]} {i[2]}", format).strftime("%H:%M") for i in res]

        y_axis = [i[3] / 100 for i in res]

        daily_max = res[-1][4]
        last_value = res[-1][3]


        return jsonify(x=x_axis, y=y_axis, max=daily_max, last=last_value), 200

    except Exception as e:
        return str(e), 200

# GitHub Webhook to automatically pull code
@app.route("/reload_app", methods=["POST"])
def reload_app():
    if request.method != "POST": return "Wrong Event Type", 400

    os.system("cd /home/bengstock/bengstock && git pull origin master")

    return "Server Reload successful.", 200
