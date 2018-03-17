import jwt
import requests
import datetime
import json
import os

URL = 'http://83.160.85.219:5000/dashboard'
TOKEN = 'cc83733cb0af8b884ff6577086b87909'

HOUR = 60*60

date_time = datetime.datetime.utcnow().replace(microsecond=0)
timestamp = int(date_time.timestamp())
isotime = date_time.isoformat().replace(':', '_')

os.makedirs(isotime)

details_endpoint = 'get_json_details'
data = requests.get('{}/{}'.format(URL, details_endpoint)).text
with open('{}/{}'.format(isotime, details_endpoint), 'w') as f:
    f.write(data)

endpoints = [
    'get_json_monitor_rules',
    'get_json_data',
    'get_json_data/{}'.format(timestamp - HOUR)
]

for endpoint in endpoints:
    uri = '{}/{}'.format(URL, endpoint)
    req = requests.get(uri)
    data = json.loads(jwt.decode(req.text, TOKEN, algorithms=['HS256'])['data'])
    
    name = '{}/{}'.format(isotime, endpoint.replace('/', '_'))

    with open(name, 'w') as f:
        f.write(json.dumps(data, indent=4))
        f.write('\n')