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
payload = {'sort': '-timestamp', 'page_size': '450'}
filename = "/tmp/total_perf.txt"
outfile = open(filename,"w")
for serial in serial_numbers:
 total = requests.get('http://'+infinimetrics_ip+'/api/rest/systems/'+serial+'/monitored_entities/1/data/', auth=HTTPBasicAuth(login,password), params=payload, verify=False)
 data = total.json()
 for timestamp in data['result']:
                                timedata = timestamp['timestamp']
                                epoch = timegm(time.strptime(timedata.replace('Z', 'UTC'),'%Y-%m-%dT%H:%M:%S%Z'))
                                read_bandwidth_MB = int(timestamp['read_bytes']) / 1048576
                                read_bandwidth_MB_rounded = round(read_bandwidth_MB,3)
                                write_bandwidth_MB = int(timestamp['write_bytes']) / 1048576
                                write_bandwidth_MB_rounded = round(write_bandwidth_MB,3)
                                print ('"',serial,'" ','infinidat.total.read.iops ',epoch,' ',int(timestamp['read_ops']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.total.write.iops ',epoch,' ',int(timestamp['write_ops']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.total.read.latency ',epoch,' ',float(timestamp['read_latency']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.total.write.latency ',epoch,' ',float(timestamp['write_latency']), sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.total.read.bandwidth ',epoch,' ',read_bandwidth_MB_rounded, sep='', file=outfile)
                                print ('"',serial,'" ','infinidat.total.write.bandwidth ',epoch,' ',write_bandwidth_MB_rounded, sep='', file=outfile)
outfile.close()
subprocess.call(["zabbix_sender", "-z", zabbixIP, "-i", filename, "-T"])
