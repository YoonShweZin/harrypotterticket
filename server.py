from flask import Flask, render_template, request
from datetime import datetime, timedelta
import json

app = Flask(__name__)

all = json.load(open('all.json'))
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/month/<mnth>")
def data(mnth):
    [yr,mn] = mnth.split('-')
    first = datetime(year=int(yr),month=int(mn),day=1)
    dopm = first - timedelta(days = first.weekday())      #predict past date
    print(dopm)
    weeks = []
    for w in range(5):
        week = []
        for i in range(7):
            day = (dopm+timedelta(days=i+7*w)).isoformat()[:10]
            week.append({
                "whn": day,
                "free": sum([x["capacity"]-x["booked"] for x in all if x["whn"].startswith(day)])
            })
        weeks.append(week)
    ret = {
        "month-name":first.strftime("%B"),            #dynamic date
        "month-year":f"{yr}",
        "weeks":weeks
    }
    return ret

@app.route("/day/<date>")
def date(date):
    t_slot = [x for x in all if x['whn'].startswith(date)]
    return {"availability":t_slot}      #return available seat with its date

@app.route("/ticket/",methods=['GET','POST'])
def booking():                                
    datetime = request.args.get("datetime")
    time = request.args.get("time")
    adult = request.args.get("adultTicket")   #get data from text box
    child = request.args.get("childTicket")
    ticketPrice = request.args.get("ticketPrice")

    return render_template("ticket.html", datetime = datetime, time = time, adult = adult, child = child, ticketPrice = ticketPrice)

app.run(debug=True, port=5568)
