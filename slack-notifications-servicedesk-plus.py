# Slack Notifications for ServiceDesk Plus

# Author
# I’m Vladimir Mikhalev, the Docker Captain, but my friends can call me Valdemar.
# https://www.docker.com/captains/vladimir-mikhalev/

# My website with detailed IT guides: https://www.heyvaldemar.com/
# Follow me on YouTube: https://www.youtube.com/channel/UCf85kQ0u1sYTTTyKVpxrlyQ?sub_confirmation=1
# Follow me on Twitter: https://twitter.com/heyValdemar
# Follow me on Instagram: https://www.instagram.com/heyvaldemar/
# Follow me on Threads: https://www.threads.net/@heyvaldemar
# Follow me on Mastodon: https://mastodon.social/@heyvaldemar
# Follow me on Bluesky: https://bsky.app/profile/heyvaldemar.bsky.social
# Follow me on Facebook: https://www.facebook.com/heyValdemarFB/
# Follow me on TikTok: https://www.tiktok.com/@heyvaldemar
# Follow me on LinkedIn: https://www.linkedin.com/in/heyvaldemar/
# Follow me on GitHub: https://github.com/heyvaldemar

# Communication
# Chat with IT pros on Discord: https://discord.gg/AJQGCCBcqf
# Reach me at ask@sre.gg

# Give Thanks
# Support on GitHub: https://github.com/sponsors/heyValdemar
# Support on Patreon: https://www.patreon.com/heyValdemar
# Support on BuyMeaCoffee: https://www.buymeacoffee.com/heyValdemar
# Support on Ko-fi: https://ko-fi.com/heyValdemar
# Support on PayPal: https://www.paypal.com/paypalme/heyValdemarCOM

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
