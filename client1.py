import requests
import json
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
DO_PIN = 3
GPIO.setup(DO_PIN, GPIO.IN)
url = "http://3.111.217.187:8080"

def send_post_request(url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url+"/api/safe", data=json.dumps(payload), headers=headers)
    return response

last4 = [0, 0, 0, 0]

while True:
    data = {
        "id": "mq2",
        "data": {
            # "timestamp": 0/1
        }
    }
    for _ in range(3): # 0.25 min = 3 times x 5 seconds
        # print("_ = ", _)
        time.sleep(5)
        gas_present = GPIO.input(DO_PIN)
        if gas_present == GPIO.LOW:# safe is 0, unsafe is 1
            data["data"][time.strftime("%d%Y-%m-%d %H:%M:%S", time.localtime())] = "0" #Wed Apr 24 13:12:28 2024
            last4.pop(0)
            last4.append(0)
        else:
            data["data"][time.strftime("%d%Y-%m-%d %H:%M:%S", time.localtime())] = "1"
            last4.pop(0)
            last4.append(1)
    print(last4)
    print(send_post_request(url, data).text)
    if last4==[1, 1, 1, 1]:
        print("sending alert")
        print(requests.get(url+"/api/unsafe").text)
