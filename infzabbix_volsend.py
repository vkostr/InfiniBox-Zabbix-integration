#!/usr/bin/env python3
import requests, time, os, sys, subprocess, urllib3
from datetime import datetime
from calendar import timegm
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
zabbixIP = "127.0.0.1"
# if many Infiniboxes monitored by one Infinimetrix use: serial_numbers = ["serial_1","serial_2","serial_x"]
serial_numbers = ["serial"]
infinimetrics_ip = "127.0.0.1"
login = 'login'
password = 'password'
payload = {'sort': '-timestamp', 'page_size': '10000'}
filename = "/tmp/vol_perf.txt"
outfile = open(filename,"w")
for serial in serial_numbers:
 vol_ids = requests.get('http://'+infinimetrics_ip+'/api/rest/systems/'+serial+'/monitored_entities/', auth=HTTPBasicAuth(login,password), params=payload, verify=False)
 data = vol_ids.json()
 for id in data['result']:
  if id['type'] == 'Volume':
   id_str = str(id['id'])
   payload2 = {'sort': '-timestamp', 'page_size': '450'}
   vol_data = requests.get('http://'+infinimetrics_ip+'/api/rest/systems/'+serial+'/monitored_entities/'+id_str+'/data/', auth=HTTPBasicAuth(login,password), params=payload2, verify=False)
   vol_name = id['name']
   vdata = vol_data.json()
   for timestamp in vdata['result']:
                                timedata = timestamp['timestamp']
                                epoch = timegm(time.strptime(timedata.replace('Z', 'UTC'),'%Y-%m-%dT%H:%M:%S%Z'))
                                read_bandwidth_MB = int(timestamp['read_bytes']) / 1048576
                                read_bandwidth_MB_rounded = round(read_bandwidth_MB,3)
                                write_bandwidth_MB = int(timestamp['write_bytes']) / 1048576
                                write_bandwidth_MB_rounded = round(write_bandwidth_MB,3)
                                print ('"',serial,'" ','infinidat.volume.read.iops[',vol_name,']',' ',epoch,' ',int(timestamp['read_ops']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.volume.write.iops[',vol_name,']',' ',epoch,' ',int(timestamp['write_ops']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.volume.read.latency[',vol_name,']',' ',epoch,' ',float(timestamp['read_latency']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.volume.write.latency[',vol_name,']',' ',epoch,' ',float(timestamp['write_latency']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.volume.read.bandwidth[',vol_name,']',' ',epoch,' ',read_bandwidth_MB_rounded, sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.volume.write.bandwidth[',vol_name,']',' ',epoch,' ',write_bandwidth_MB_rounded, sep='', file=outfile)
outfile.close()
subprocess.call(["zabbix_sender", "-z", zabbixIP, "-i", filename, "-T"])
