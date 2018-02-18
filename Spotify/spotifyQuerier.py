import requests
import json


def authenticate():
	auth_url = 'https://accounts.spotify.com/api/token'

	with open('auth.txt', 'r') as f:
		content = f.readlines()
		content = [x.strip() for x in content] 
		refresh_code = content[0]
		clientid = content[1]
		clientsecret = content[2]	

	headers = {'Content-Type':'application/x-www-form-urlencoded'}
	params = dict(
		grant_type = 'refresh_token',
		refresh_token = refresh_code,
		redirect_uri = 'http://tobyjames.xyz',
		client_id = clientid,
		client_secret = clientsecret
		)
	f.close()
	response = requests.post(url = auth_url, params = params, headers = headers)
	if 'refresh_token' in response.json():
		f = open('auth.txt', 'w')
		content[0] = response.json()['refresh_token']
		f.writelines(content)
	print(response.status_code)
	return response.json()['access_token']

	
	



def search(track_list):
	
	auth_code = authenticate()

	headers = {'Authorization' : auth_code}
	
	url = 'https://api.spotify.com/v1/search'

	for track in track_list:
	
		params = dict(
			q = str(track).replace(" ", "%20"),
			type = "track",
			limit = '5')

		response = requests.get(url = url, headers = headers, params = params)
	return response
#authenticate()
print(authenticate())
