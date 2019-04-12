import requests
import csv
from urllib.parse import urlencode
from pprint import pprint

domain = 'https://sandbox.tinypass.com'
aid = 'o1sRRZSLlw'
api_token = 'zziNT81wShznajW2BD5eLA4VCkmNJ88Guye7Sw4D'

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "application/json",
    }

combined = []
with open("file_a.csv") as f:
	file_a = [{k: v for k, v in row.items()}
		for row in csv.DictReader(f)]
with open("file_b.csv") as f:
	file_b = [{k: v for k, v in row.items()}
		for row in csv.DictReader(f)]

for row_a in file_a:
	for row_b in file_b:
		if row_a['user_id'] == row_b['user_id']:
			row_a.update(row_b)
			row_a['uid'] = row_a.pop('user_id')
			combined.append(row_a)
			break

get_users_url = f'{domain}/api/v3/publisher/user/list'
data = {'aid': aid, 'offset': 0, 'api_token': api_token}
form_data = urlencode(data)
response = requests.post(get_users_url, data=form_data, headers=headers)
users = response.json()['users']

users_to_add = []
for user in users:
	for row in combined:
		if user['email'] == row['email']:
			row['uid'] = user['uid']

pprint(combined)

with open('results.csv','w') as output_file:
	w = csv.DictWriter(output_file,combined[0].keys())
	w.writeheader()
	w.writerows(combined)


create_user_path = f'{domain}/api/v3/publisher/user/create'
for user in combined:
	user['aid'] = aid
	user['api_token'] = api_token
	response = requests.post(create_user_path, data=user, headers=headers)
	print(response.json())



# get_user_url = f'{domain}/api/v3/publisher/user/get'
# for user in combined:
# 	user_data = {k: v for k, v in user.items() 
# 		if k in ('uid', 'aid', 'api_token')}
# 	form_data = urlencode(user_data)
# 	response = requests.post(get_user_url, data=form_data, headers=headers)
# 	print(response.json())
