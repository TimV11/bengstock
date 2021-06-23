import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import mysql.connector
from twilio.base.exceptions import TwilioRestException

from whatsapp_tim_lin import send_wa

def get_soup(stock):
    stocks = {"estx":r"https://de.finance.yahoo.com/quote/%5ESTOXX50E?p=%5ESTOXX50E", "silber":""}
    result = requests.get(stocks.get(stock))
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    return soup

def curr_stockvalue(stock):
    soup = get_soup(stock)
    current_value = int(soup.find_all("span", {"class": "Trsdu(0.3s)", "data-reactid": "32"})[0].text.replace(",","").replace(".",""))
    return current_value

def daily_high(stock):
    soup = get_soup(stock)
    daily_high = int(soup.find("div", id="quote-summary").find_all("div")[1].find("tbody").find_all("tr")[0].find_all("td")[1].text.split(" - ")[1].replace(",","").replace(".",""))
    return daily_high

mydb = mysql.connector.connect(host="bengstock.mysql.pythonanywhere-services.com", user="bengstock", password="tomtimsql", database="bengstock$default")

while True:
    curr = curr_stockvalue("estx")
    high = daily_high("estx")
    now = datetime.now()
    hour= now.hour +2 #weil zeitverschiebung
    minute = now.minute
    weekday = now.weekday()
    currtime = f"{hour}.{minute}"
    if (hour == 17 and minute >= 55) or (weekday>4 and hour == 17):
        try: send_wa("Bot läuft 24h")
        except TwilioRestException:
            pass

    if hour >= 18 or hour < 8 or weekday > 4:
        time.sleep(3600)
        continue

    if curr < (high * 0.992):
        try: send_wa("Found! The current Stock value is 0.8% lower than the daily maximum.")
        except TwilioRestException:
            pass

    try:
        mydb.reconnect()
        mycursor = mydb.cursor()
        sql = f"INSERT INTO data (date, time, curr_val, daily_max) VALUES ( NOW(), {currtime} , {curr}, {high});"
        mycursor.execute(sql)
        mydb.commit()
    except Exception as e: print(e)
    print(mycursor.rowcount, "record inserted.")
    time.sleep(300)
