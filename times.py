from bs4 import BeautifulSoup as bs


from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import requests
import os.path
import datetime

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

except ImportError:
	flags = None

SCOPES = ['https://www.googleapis.com/auth/calendar']
store = file.Storage('storage.json')
creds = store.get()


times = ['fajr', 'shuruk', 'dhuhr', 'asr', 'maghrib', 'isha']


# if no valid creds, let user login
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store, flags)


serv = build('calendar', 'v3', http=creds.authorize(Http()))



# Getting data from salah.dk ;D
page = requests.get('http://salah.dk')

soup = bs(page.content, 'html.parser')
res = soup.find(id='times')

res = res.find_all('dl')



now = datetime.datetime.now()
now2 = datetime.datetime.utcnow().isoformat() + 'Z'

list = serv.events().list(calendarId='primary', maxResults=10, timeMin=now2, singleEvents=True, orderBy='startTime').execute()
events_list = list.get('items', [])

if not events_list:
	print("Proceeding")

for event in events_list:
	for i in range(5):
		if event['summary'] == times[i]:
			print(event['id'])
			serv.events().delete(calendarId='primary', eventId=event['id'])


for i in res:

	event = {
		'summary': i.dd.text,
		'start': {
			'dateTime': now.strftime('%Y-%m-%dT') + i.dt.text + ':00',
			'timeZone': 'Europe/Copenhagen',
		},
		'end': {
			'dateTime': now.strftime('%Y-%m-%dT') + i.dt.text + ':09',
			'timeZone': 'Europe/Copenhagen'
		},
		'attendees': [
			{
				'email': 'syedmshaaf@gmail.com'
			}
		]
	}

	e = serv.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()


