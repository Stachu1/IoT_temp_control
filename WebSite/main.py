from flask import Flask, redirect, url_for, request, render_template, Blueprint, flash, make_response
from threading import Thread
from datetime import datetime
import os, json, pytz, secrets, time, random


app = Flask(__name__)

measurments_history = 288

records = [[datetime.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d %H:%M:%S"), 0]]
x = []
for i in range(measurments_history):
    x.append(round(-measurments_history/12+(i+1)/12, 2))

y = []
for i in range(measurments_history):
    y.append(0)

heating_history = []
for i in range(measurments_history):
    heating_history.append(0)

zero = []
for i in range(measurments_history):
    zero.append(0)

# print(x)
# print(y)
# print(zero)

heater = [0]

temp_target = [-100]

password = "password"

token = [secrets.token_hex(nbytes=16)]


@app.route("/", methods=["POST", "GET"])
def home():
    if request.cookies.get("token") == token[0]:
        if request.method == "POST":
            try:
                temp_target[0] = int(request.form.get("Temp_target"))
            except:
                pass
            if float(records[0][1]) < temp_target[0]:
                heater[0] = 1
            elif float(records[0][1]) > temp_target[0] + 1:
                heater[0] = 0
        return render_template("home.html", content=records, x=x, y=y, zero=zero, temp_target=temp_target, heater=heater, heating_history=heating_history)
    else:
        return redirect("login")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form.get("password") == password:
            resp = make_response(redirect("/"))
            resp.set_cookie("token", token[0])
            return resp
        else:
            message = "Incorrect password!"
            return render_template("login.html", content=message)
    message = ""
    return render_template("login.html", content=message)


@app.route("/post", methods=["POST"])
def post():
    data = request.data.decode("utf-8").split(";")
    # print(data)
    temp = float(data[0]) - 1
    presure = float(data[1])
    if len(records) == 288:
        records.pop(-1)
    if len(x) == 288:
        x.pop(-1)
    if len(y) == 288:
        y.pop(0)
    if len(heating_history) == 288:
        heating_history.pop(0)

    y.append(temp)

    heating_history.append(heater[0])

    records.insert(0, [datetime.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d %H:%M:%S"), temp])
    print(f"Data-index[{len(records)}] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {temp}")
    return ""


@app.route("/heater")
def heater_state():
    return str(heater[0])



def heater_refresh(delay):
    while True:
        time.sleep(delay)
        if float(records[0][1]) < temp_target[0]:
            heater[0] = 1
        elif float(records[0][1]) > temp_target[0] + 3:
            heater[0] = 0


def token_refresh(delay):
    while True:
        time.sleep(delay)
        token[0] = secrets.token_hex(nbytes=16)
        print(f"New token: {token[0]}")


if __name__ == '__main__':
    token_refresh_thread = Thread(target=token_refresh, args=(3600,))
    token_refresh_thread.start()
    heater_refresh_thread = Thread(target=heater_refresh, args=(60,))
    heater_refresh_thread.start()

    app.run(debug=False, host="0.0.0.0", port=6060)