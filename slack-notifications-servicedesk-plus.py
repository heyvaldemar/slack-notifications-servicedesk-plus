# Slack Notifications for ServiceDesk Plus

# Vladimir Mikhalev
# callvaldemar@gmail.com
# www.heyvaldemar.com

import requests
import sys
import json
import datetime

filename = str(sys.argv[1])

with open(filename) as data_file:
	data = json.load(data_file)
requestObj = data['request']

# ServiceDesk Plus URL (replace with yours)
url="https://sdp.heyvaldemar.net"

workorderid = requestObj['WORKORDERID']
requester = requestObj['REQUESTER']
createdby = requestObj['CREATEDBY']
priority = requestObj['PRIORITY']
subject =  requestObj['SUBJECT']

# Slack channel to post notifications from ServiceDesk Plus (replace with yours)
channel = "#it-team-tickets"

CREATEDTIME = requestObj['CREATEDTIME']
scheduledstarttime = datetime.datetime.fromtimestamp(int(CREATEDTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')

# Message to post in the Slack channel (replace with yours)
payload='{"channel": "'+channel+'", "text": "hey guys, a new request has been created \n Subject: ' + subject + '\n Requester: ' + requester + '\n Priority: ' + priority + '\n Link: ' + url +'/WorkOrder.do?woMode=viewWO&woID='+workorderid+'"}'
jsondata=json.dumps(payload)

headers = {'content-type': 'application/x-www-form-urlencoded'}

with requests.Session() as s:

	# Slack incoming URL (replace with yours)
	url = "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX"
	r = s.post(url,verify=True, data={"payload" :payload},headers=headers)

resultjson={}

if r.text=='ok':
	resultjson["result"]="success"
	resultjson["message"]="Notification posted to Slack Successfully"
	print(resultjson)
else:
	resultjson["result"]="failure"
	resultjson["message"]="Error Posting notification to Slack"
	print(resultjson)
