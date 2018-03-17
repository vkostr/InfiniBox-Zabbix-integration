# InfiniBox-Zabbix-integration
InfiniBox Zabbix integration
Zabbix integration with Infinidat Infinimetrics monitoring tool

Integration structure
Template is imported in Zabbix, which uses scripts in Python 3.x (Discovery rules) to populate the Host object (InfiniBox) with objects (Items, Graphs). Objects are taken from Infinimetrics by the REST API. Separately, using, for example, cron, Python 3.x scripts run periodically, which populate Items with performance data from Infinimetrics using zabbix_sender.

Setup Instructions
Place the discovery scripts (infzabbix_*list.py, zbxhostname.sh) in the appropriate Zabbix directory (usually/usr/lib/zabbix/externalscripts). Edit these scripts. Discovery scripts contain the variables “login” and “password” to connect to InfiniMetrics. It is recommended to create a special user with read only permissions and use its credentials. Verify that scripts from the user zabbix with InfiniBox serial and infinimetrix_ip parameters give normal JSON (can be checked through JSON Validator https://jsonlint.com/).
Import the Template InfiniBox in Zabbix. In the template there is a macro, $INFINIMETRICS_IP. $INFINIMETRICS_IP must necessarily be changed to the actual one.
Create Host objects for the InfiniBox storage system in Zabbix. Host name must be equal to the serial number, for example, 1499. Visible name can be any. In the template there are sections for filling objects such as volumes, file systems and servers. Not needed object types can be removed, if necessary. The retention period for all objects is 180 days, you can correct it as necessary (find and replace <history>180</history> with the required parameter).
Discovery is configured to run every 2 minutes to start quickly. As soon as the initial discovery occurs, it must be changed for a longer period, for example, 4 hours. Similarly, for item "Infinibox hostname" you should increase interval too. "Infinibox hostname" item is a workaround for filling the name of the graphs with the name of the storage system.
Place and configure the start of scripts to fill objects with data (infzabbix_* send.py). The scripts for filling in objects with data contain the variables “login” and “password” for connection to InfiniMetrics, and variables “infinimetrix_ip” and “serial” - it must to be changed to the actual ones. It is recommended to create a special user with read only permissions and use its credentials. Also in such scripts used the variable zabbixIP = 127.0.0.1 is used, if the scripts are not running from the Zabbix server, then it must be edited to the actual IP.
The scripts for filling objects with data are intended to run from cron, because Zabbix has a short timeout for the script, and it does not have enough time to execute. Scripts are configured to run every hour, if you plan to run more often / less often, you need to correct the page_size field for payload2, and considering that the smallest record granularity in InfiniMetrics is 10 seconds. The field has a limit of 10,000 records, if you need more, then you need to use several pages for the query. The value should be set more than the crom run interval to add the execution time of the script itself.

Was tested at SW below and using the following python modules
Python 3.4.3, modules requests 2.18.4, urllib3 1.22, pip 9.0.1 (for installing modules)
https://pypi.python.org/pypi/requests/2.18.4
https://pypi.python.org/pypi/urllib3/1.22
https://bootstrap.pypa.io/get-pip.py

Zabbix Appliance 3.0

