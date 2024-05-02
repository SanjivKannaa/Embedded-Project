from flask import Flask, render_template, request, jsonify
import mysql.connector as sql
from twilio.rest import Client
import env
import time
import datetime

creds = {
    "sanjiv": "sanjiv",
    "krupa": "krupa",
    "appruval": "appruval"
}


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


@app.get("/login")
def login():
    return render_template("login.html", error="")

@app.post("/login")
def login_action():
    username = request.form['username']
    password = request.form['password']
    global creds
    if username in creds.keys():
        if creds[username]==password:
            return app.redirect("/dashboard")
        else:
            return render_template("login.html", error="wrong password")
    return render_template("login.html", error="user not identified")


@app.get("/dashboard")
def dashboard():
    last_leak = ""
    mq2_count = 0
    mq3_count = 0
    mq4_count = 0
    row_count = 0
    table_data = ""
    t1 = env.mysqltablename1
    t2 = env.mysqltablename2
    t3 = env.mysqltablename3
    try:
        query = '''
        SELECT
        {}.timestamp,
        {}.value AS {}value,
        {}.value AS {}value,
        {}.value AS {}value
        FROM {}
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        ORDER BY timestamp DESC'''.format(t1, t1, t1, t2, t2, t3, t3, t1, t2, t1, t2, t3, t2, t3)
        cur.execute(query)
        # last_leak = str(cur.fetchall()[0][3])
        data = cur.fetchall()
        for i in data:
            if "1" in i[1:]:
                last_leak = i[0] + " "
                if i[1] == "1":
                    last_leak += t1 + " and "
                if i[2] == "1":
                    last_leak += t2 + " and "
                if i[3] == "1":
                    last_leak += t3 + " and "
                break
        last_leak = last_leak[:-4]
    except:
        pass
    try:
        # get total row count
        query = '''SELECT COUNT(*) FROM {}'''.format(t1)
        cur.execute(query)
        row_count = cur.fetchall()[0][0]
    except:
        pass
    try:
        current_time = datetime.datetime.now()
        thirty_days_ago = current_time - datetime.timedelta(days=30)
        formatted_time = thirty_days_ago.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("SELECT count(*) from {} where value=1 and timestamp>'{}'".format(t1, formatted_time))
        mq2_count = cur.fetchall()[0][0]
    except:
        pass
    try:
        current_time = datetime.datetime.now()
        thirty_days_ago = current_time - datetime.timedelta(days=30)
        formatted_time = thirty_days_ago.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("SELECT count(*) from {} where value=1 and timestamp>'{}'".format(t2, formatted_time))
        mq3_count = cur.fetchall()[0][0]
    except:
        pass
    try:
        current_time = datetime.datetime.now()
        thirty_days_ago = current_time - datetime.timedelta(days=30)
        formatted_time = thirty_days_ago.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("SELECT count(*) from {} where value=1 and timestamp>'{}'".format(t3, formatted_time))
        mq4_count = cur.fetchall()[0][0]
    except:
        pass
    try:
        # get table data
        table_data = []
        query = '''
        SELECT
        {}.timestamp,
        {}.value AS {}value,
        {}.value AS {}value,
        {}.value AS {}value
        FROM {}
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        ORDER BY timestamp DESC'''.format(t1, t1, t1, t2, t2, t3, t3, t1, t2, t1, t2, t3, t2, t3)
        cur.execute(query)
        table_data = list(cur.fetchall())
        if table_data == []:
            table_data = [["EMPTY", "TABLE"]]
    except:
        table_data = [["ERROR", "GETTING", "DATA"]]
    return render_template("dashboard.html", last_leak=last_leak, row_count=row_count, mq2_count=mq2_count, mq3_count=mq3_count, mq4_count=mq4_count, table_data=table_data)

@app.get("/clear_data")
def clear_data():
    cur.execute("delete from {}".format(env.mysqltablename1))
    cur.execute("delete from {}".format(env.mysqltablename2))
    cur.execute("delete from {}".format(env.mysqltablename3))
    mydb.commit()
    return app.redirect("/dashboard")

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
    except Exception as e:
        return "ERROR"+str(e)


@app.get("/api/unsafe")
def unsafe_handler():
    try:
        # time.sleep(10)
        message_body = "A gas leak gas been detected in the smart gas leak detection system.\nActivity in the last 1 min:\nTIMESTAMP     GAS1 GAS2 GAS3"
        t1 = env.mysqltablename1
        t2 = env.mysqltablename2
        t3 = env.mysqltablename3
        query = '''
        SELECT
        {}.timestamp,
        {}.value AS {}value,
        {}.value AS {}value,
        {}.value AS {}value
        FROM {}
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        LEFT JOIN {} ON {}.timestamp = {}.timestamp
        ORDER BY timestamp DESC LIMIT 6'''.format(t1, t1, t1, t2, t2, t3, t3, t1, t2, t1, t2, t3, t2, t3)
        cur.execute(query)
        empty_db = True
        for i in cur.fetchall():
            empty_db = False
            message_body += "\n" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3])
        if empty_db:
            message_body += "<NO LOGS>"
        message_body += "\nFor more info, login into your dashboard at {}/login".format(env.backend_url)
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        return "alert sent"
    except Exception as e:
        return "ERROR"+str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)