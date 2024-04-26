""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import requests, urllib3, os,json

urllib3.disable_warnings()
from dotenv import load_dotenv
load_dotenv()
host = os.environ['VMA_HOST']
USERNAME= os.environ['VMA_USER']
PASSWORD= os.environ['VMA_PASSWORD']

url = f"https://{host}/j_security_check"
headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
data = f"j_username={USERNAME}&j_password={PASSWORD}"
response=requests.post(url, headers=headers, data=data, verify=False)
c=response.headers['set-cookie']

url = f"https://{host}/dataservice/device"
headers = {
        "Content-Type" : "application/json", 
        "Cookie": c
    }
devices_list=[]
devices = requests.get(url, headers=headers, verify=False).json()['data']
for device in devices:
    entry={}
    entry={'deviceName':device['host-name'],'deviceId':device['uuid']}
    devices_list.append(entry)

# print(json.dumps(devices_list, indent=2))

