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

import sqlite3
from sqlite3 import Error
from create_mappings import templates_list
import json
import yaml
from get_devices import devices_list
from dotenv import load_dotenv
load_dotenv()
import os

YML_FILE = os.environ['PLAYBOOK_PATH']
DB_PATH = os.environ['DB_PATH']

def create_connection(db_file):
    """ Create DB Connection object """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def querySpecific(conn):
    map_templates_to_devices=[
        {
            'templateName':'BS-Config-C1121-DHCP-Test-Roaa',
            'devices':[]
        },
        {
            'templateName':'BS-Config-C1121-PPPoE-Test-Roaa',
            'devices':[]
        },
        {
            'templateName':'BS-Config-C1121-Test-Roaa',
            'devices':[]
        }
    ]

    c = conn.cursor()
    query_result = c.execute(f"SELECT router FROM bss").fetchall()
    routers_list=[]
    for q in query_result:
            routers_list.append(q[0])

    for router in routers_list:
        for r in map_templates_to_devices:
            if router in r['devices']:
                r[router]=[]
                sys_ip_query=c.execute(f"SELECT SDWAN_SYSTEM_IP FROM bss WHERE router='{router}'").fetchall()
                sys_ip=str(sys_ip_query[0][0])
                for t in templates_list[r['templateName']]:
                    query_result = c.execute(f"SELECT {t[0]} FROM bss WHERE router='{router}'").fetchall()
                    if ("Vlan" in str(t[1])) and (str(query_result[0][0]) != "NA"):
                        ii2=str(t[1]).removesuffix('ip/address')
                        ii2=ii2+"shutdown"
                        r[router].append({str(t[1]):str(query_result[0][0])})
                        r[router].append({ii2:"false"})
                    elif ("Vlan" and "/interface/ip/address" in str(t[1])) and (str(query_result[0][0]) == "NA"):
                        sys_ipp=sys_ip.split('.')
                        sys_ipp[3]=int(sys_ipp[3])+1
                        dummy_ip=sys_ipp[0]+'.'+sys_ipp[1]+'.'+sys_ipp[2]+'.'+str(sys_ipp[3])+'/30'
                        ii2=str(t[1]).removesuffix('ip/address')
                        ii2=ii2+"shutdown"
                        r[router].append({str(t[1]):dummy_ip})
                        r[router].append({ii2:"true"})
                    elif str(t[1])=="csv-deviceId":
                        for d in devices_list:
                            if d['deviceName']==router:
                                deviceId=d['deviceId']
                                r[router].append({str(t[1]):deviceId})
                    else:
                        r[router].append({str(t[1]):str(query_result[0][0])})
    return map_templates_to_devices
def close_connection(conn):
    conn.close()


def modify_yml(map_templates_to_devices):
    with open(YML_FILE, 'r') as stream:
        try:
            loaded = yaml.load(stream,Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    for t in map_templates_to_devices:
        if len(t['devices'])!=0:
            for device in t['devices']:
                my_data=loaded[0]['roles']
                r=len(my_data)
                my_data.append({'role':'attach_device_template','vars':{'DeviceTemplateList':{t['templateName']:[{'csv-deviceId':'XYZ'}]}}})
                with open(YML_FILE, 'w') as stream:
                    try:
                        yaml.dump(loaded, stream, default_flow_style=False)
                    except yaml.YAMLError as exc:
                        print(exc)
                my_data=loaded[0]['roles'][r]['vars']['DeviceTemplateList'][t['templateName']][0]
                for dd in t[device]:
                        for d in dd:
                            my_data[d]=dd[d]

    # Save it again
    with open(YML_FILE, 'w') as stream:
        try:
            yaml.dump(loaded, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)



if __name__ == "__main__":
    conn = create_connection(DB_PATH)
    if conn is not None:      
        map_templates_to_devices=querySpecific(conn)
        modify_yml(map_templates_to_devices)
            # print(json.dumps(map_templates_to_devices, indent=2))
        close_connection(conn)
        # print(devices_list)
    


