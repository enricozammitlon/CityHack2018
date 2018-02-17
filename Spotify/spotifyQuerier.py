import requests
import json


def authenticate():
	auth_url = 'https://accounts.spotify.com/authorize'
params = dict(
	'client_id' = '18d5540610164219adcaede028711873',
	'redirect_uri' = 'http://tobyjames.xyz'
	)
	

	return auth_code


def search(track_list):
	
	auth_code = authorise()

	headers = {'Authorization' : auth_code}
	
	url = 'https://api.spotify.com/v1/search'

	for track in track_list:
	
		params = dict(
			'q' = str(track).replace(" ", "%20"),
			'type' = "track"i,
			'limit' = '5')

		response = requests.get(url = url, headers = headers, params = params)


