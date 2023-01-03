import requests, json
import os
import vobject
from dateutil.parser import parse

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    return data


token = os.environ['TOKEN']
databaseId = os.environ['DB_ID']


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

result = readDatabase(databaseId, headers)

cal = vobject.iCalendar()
for t in result['results']:
    pr = t['properties']
    vevent = cal.add('vevent')
    vevent.add('summary').value = pr['Name']['title'][0]['text']['content']
    vevent.add('dtstart').value = parse(pr['Date']['date']['start'])
    if pr['Date']['date']['end'] is not None:
        vevent.add('dtend').value = parse(pr['Date']['date']['end'])
    # TODO add URL
    # if pr['URL']['url'] is not None:
    #     vevent.add['URL'].value = pr['URL']['url']