#i--------------------------------------------------------------------
# Spotify API caller by Toby James
# tobyswjames@gmail.com - tbyjms.me
#--------------------------------------------------------------------

import requests
import json
import time

# Authenticates against OAuth 2.0 to allow access to Spotify's API

def authenticate():
	auth_url = 'https://accounts.spotify.com/api/token'

	with open('/var/www/html/tubeamp.me/app/.htauth.txt', 'r') as f:			# Authentication data stored in seperate file
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
		client_secret = clientsecret,
		scope = 'playlist-modify-public'
		)
	f.close()
	response = requests.post(url = auth_url, params = params, headers = headers)

	print("Authenticate: " + str(response.status_code))    # Print calls throughout file display progress of various HTTP verbs as the program runs

	if 'refresh_token' in response.json():
		f = open('/var/www/html/tubeamp.me/app/.htauth.txt', 'w')
		content[0] = response.json()['refresh_token']
		f.writelines(content)
	return response.json()['access_token']

	
# Returns the information about tracks received as an array of track IDs. Authentication code
# is passed through all functions for authentication, so authenticate() is only called once

def getTrackInfo(track_list, auth_code):

	headers = {'Authorization' : "Bearer " + auth_code}
	
	url = 'https://api.spotify.com/v1/tracks'

	time_list = []
	artist_list = []
	uri_list = []
	popularity_list = []

	while len(track_list) >= 50:
		del track_list[::5]

	track_list = ",".join(track_list)
	
	params = dict(ids = track_list)

	response = requests.get(url = url, headers = headers, params = params)

	print("getTrackInfo: " + str(response.status_code))

	for track in response.json()['tracks']:

		time_list.append(track['duration_ms'])

		uri_list.append(track['uri'])

		artist_list.append(track['album']['artists'][0]['name'])

		popularity_list.append(track['popularity'])

	track_dict = dict(
		artist = artist_list,
		uri = uri_list,
		time = time_list,
		popularity = popularity_list)

	return track_dict	

# Creates and populates a playlist of songs it is given.
# Sorts the songs by popularity.

def createPlaylist(track_dict, journey_time, auth_code):

	artists = track_dict['artist']
	uris = track_dict['uri']
	times = [int(k) for k in track_dict['time']]
	popularities = track_dict['popularity']	
	uri_list = []

#Sort songs by popularity, add the most popular ones to the list to be added to the playlist
#aims to avoid adding songs by the same artist by passing through the list until it is empty or the time limit is reached
	unsortedArray = []
	for i in range(len(artists)):
		unsortedArray.append([artists[i], uris[i], times[i], popularities[i]])

	time_total = 0
	artist_list = []
	sortedArray= sorted(unsortedArray,key=lambda unsortedArray: unsortedArray[3], reverse=True);

	while time_total < journey_time:
		artists_list = []
		for item in sortedArray:
			print(item)
			if item[0] not in artists_list:
				print("Added, time = ", time_total, "Journey time = ", journey_time)
				uri_list.extend([item[1]])
				time_total += item[2]
				artist_list.extend([item[0]])
			
			if time_total > journey_time:
				break
#Create a playlist

	url = 'https://api.spotify.com/v1/users/p4jjeadeuvo4zp30dt9krbx24/playlists'	
	headers = {'Authorization':"Bearer "+ auth_code, 'Content-Type': 'application/json'}
		   
	data = dict(
			name = time.ctime(),
			public = 'true'
		   )

	response = requests.post(url = url, headers = headers, data = json.dumps(data))

	print("Create Playlist: " + str(response.status_code))

	playlist_url = response.json()['external_urls']['spotify']

	playlist_id = response.json()['id']


#Populate playlist with preselected songs

	populate_headers = {'Authorization':"Bearer "+ auth_code, 'Accept': 'application/json'}
	populate_url = "https://api.spotify.com/v1/users/p4jjeadeuvo4zp30dt9krbx24/playlists/" + playlist_id + "/tracks/"
	populate_data = dict(
			uris = uri_list
			)

	populate_response = requests.post(url = populate_url, headers = populate_headers, data = json.dumps(populate_data))
	print(populate_response.status_code)
	return playlist_url

# Master function, takes input from TFL, calls authenticate() and passes the call down the whole chain.
	
def search(track_list, journey_time):
	
	journey_time = journey_time*60000

	auth_code = authenticate()

	headers = {'Authorization' : "Bearer " + auth_code}
	
	url = 'https://api.spotify.com/v1/search'

	response_list = []

	for track in track_list:
		
		if "Underground Station" in track:
			track = track[:-20]
		print(track)
		
		params = dict(
			q = str(track).replace(" ", "+"),
			type = "track",
			limit = '10')


		response = requests.get(url = url, headers = headers, params = params)
		for item in response.json()['tracks']['items']:
			response_list.append(item['id'])
	print("Get tracks by id: " + str(response.status_code))
	info = getTrackInfo(response_list, auth_code)

	playlist_url = createPlaylist(info, journey_time, auth_code)

	return playlist_url
