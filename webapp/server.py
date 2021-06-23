from flask import Flask, render_template

import mysql.connector

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

    y_axis = [i[3] for i in res]

    daily_max = res[-1][4]
    last_value = res[-1][3]

    return render_template("home.html", x=x_axis, y=y_axis, max=daily_max, last=last_value, res=res)