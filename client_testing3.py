import requests
import json
import time
# import RPi.GPIO as GPIO
import random

# GPIO.setmode(GPIO.BCM)
# DO_PIN = 7
# GPIO.setup(DO_PIN, GPIO.IN)
url = "http://3.111.217.187:8080"

def send_post_request(url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url+"/api/safe", data=json.dumps(payload), headers=headers)
    return response

last4 = [0, 0, 0, 0]

while True:
    data = {
        "id": "mq4",
        "data": {
            # "timestamp": 0/1
        }
    }
    for _ in range(3): # 0.5 min = 3 times x 10 seconds
        time.sleep(1)
        # gas_present = GPIO.input(DO_PIN)
        if random.randint(0, 1): #gas_present == GPIO.LOW:# safe is 0, unsafe is 1
            data["data"][time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())] = "0"
            last4.pop(0)
            last4.append(0)
        else:
            data["data"][time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())] = "1"
            last4.pop(0)
            last4.append(1)
    print(last4)
    print(send_post_request(url, data).text)
    if last4==[1, 1, 1, 1]:
        print("sending alert")
        print(requests.get(url+"/api/unsafe").text)
