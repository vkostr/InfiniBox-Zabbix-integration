#!/usr/bin/env python3
import json
import sys, requests, time, os, urllib3
from datetime import datetime
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
serial = str(sys.argv[1])
imx = str(sys.argv[2])
login = 'login'
password = 'password'
payload = {'sort': '-timestamp', 'page_size': '10000'}
r = requests.get('http://'+imx+'/api/rest/systems/'+serial+'/monitored_entities/', auth=HTTPBasicAuth(login,password), params=payload, verify=False)
data = r.json()
jdata = []
for id in data['result']:
	if id['type'] == 'Volume':
		jdata.append({"{#VOLUMENAME}":id['name']})
print(json.dumps({"data":jdata}))
