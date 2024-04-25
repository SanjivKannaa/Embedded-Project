from flask import Flask, render_template, request, jsonify
import mysql.connector as sql
from twilio.rest import Client
import env
import time

try:
    mydb = sql.connect(
        host=env.mysqlhost,
        user=env.mysqluser,
        password=env.mysqlpass,
        database=env.mysqldb
    )
    cur = mydb.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS {} (timestamp VARCHAR(20), value varchar(1))'''.format(env.mysqltablename1))
    cur.execute('''CREATE TABLE IF NOT EXISTS {} (timestamp VARCHAR(20), value varchar(1))'''.format(env.mysqltablename2))
    cur.execute('''CREATE TABLE IF NOT EXISTS {} (timestamp VARCHAR(20), value varchar(1))'''.format(env.mysqltablename3))
    print("DB CONNECTED SUCCESSFULLY")
except:
    print("DB CONNECTION FAILED")
    time.sleep(5)
    exit()


try:
    account_sid = env.account_sid
    auth_token = env.auth_token
    twilio_phone_number = env.twilio_phone_number
    to_phone_number = env.to_phone_number
    client = Client(account_sid, auth_token)
    print("SMS CLIENT SUCCESSFULLY")
except:
    print("SMS CLIENT CONNECTION FAILED")
    exit()

app =  Flask(__name__)
@app.get("/")
def home():
    return render_template("home.html", backend_url=env.backend_url)

@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.post("/api/safe")
def safe_handler():
    try:
        data = dict(request.json)
        device_id = data["id"]
        keys = list(data["data"].keys())
        values = list(data["data"].values())
        for i in range(len(keys)):
            query = '''INSERT INTO {} values("{}", "{}")'''.format(device_id, keys[i], values[i])
            cur.execute(query)
        mydb.commit()
        return 'Data added to database!'
    except:
        return "ERROR"


@app.get("/api/unsafe")
def unsafe_handler():
    try:
        # time.sleep(10)
        message_body = "A gas leak gas been detected in the smart gas leak detection system.\nActivity in the last 1 min:\nTIMESTAMP     GAS1 GAS2 GAS3"
        query = '''SELECT timestamp, value FROM ( SELECT timestamp, value as {} FROM {} UNION SELECT timestamp, value as {} FROM {} UNION SELECT timestamp, value as {} FROM {} ) AS all ORDER BY timestamp DESC LIMIT 6'''.format(env.mysqltablename1, env.mysqltablename1, env.mysqltablename2, env.mysqltablename2, env.mysqltablename3, env.mysqltablename3)
        cur.execute(query)
        empty_db = True
        for i in cur.fetchall():
            empty_db = False
            message_body += "\n" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3])
        if empty_db:
            message_body += "<NO LOGS>"
        message_body += "\nFor more info, login into your dashboard at gasdetector.magickite.tech/dashboard"
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        return "alert sent"
    except:
        return "ERROR"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)