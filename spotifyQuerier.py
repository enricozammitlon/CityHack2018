import requests
import json
import time

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
		client_secret = clientsecret,
		scope = 'playlist-modify-public'
		)
	f.close()
	response = requests.post(url = auth_url, params = params, headers = headers)

	print("Authenticate: " + str(response.status_code))

	if 'refresh_token' in response.json():
		f = open('auth.txt', 'w')
		content[0] = response.json()['refresh_token']
		f.writelines(content)
	return response.json()['access_token']

	
def getTrackInfo(track_list, auth_code):

	headers = {'Authorization' : "Bearer " + auth_code}
	
	url = 'https://api.spotify.com/v1/tracks/'

	time_list = []
	artist_list = []
	uri_list = []
	popularity_list = []

	track_list = ",".join(track_list)

	params = dict(ids = track_list)

	response = requests.get(url = url, headers = headers, params = params)

	print("getTrackInfo: " + str(response.status_code))

	print(response.json())

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

def createPlaylist(track_dict, journey_time, auth_code):

	artists = track_dict['artist']
	uris = track_dict['uri']
	times = [int(k) for k in track_dict['time']]
	popularities = track_dict['popularity']	

	sorted_pops = sorted(popularities, reverse=True)
	sorted_uris = uris
	sorted_times = times
	sorted_artists = artists
#Sort songs by popularity, add the most popular ones to the list to be added to the playlist
#aims to avoid adding songs by the same artist by passing through the list until it is empty or the time limit is reached

	for i in range(len(sorted_pops)):
		sorted_uris[i] = uris[popularities.index(sorted_pops[i])]
		sorted_times[i] = times[popularities.index(sorted_pops[i])]
		sorted_artists[i] = artists[popularities.index(sorted_pops[i])]
	artist_list = []
	uri_list = []
	time_list = []
	
	while sum(time_list) < journey_time:
		artist_list_temp = []
		uri_list_temp = []
		time_list_temp = []
		for i in range(len(sorted_pops)):
			if sorted_artists[i] not in artist_list_temp:
				uri_list_temp.append(sorted_uris[i])
				artist_list_temp.append(sorted_artists[i])
				time_list_temp.append(sorted_times[i])
				sorted_uris[i] = None
				sorted_artists[i] = None
				sorted_times[i] = None
				sorted_pops[i] = None
		
		sorted_uris_2 = [x for x in sorted_uris if x != None]
		sorted_artists_2 = [y for y in sorted_artists if y != None]
		sorted_times_2 = [z for z in sorted_times if z != None]
		sorted_pops_2 = [w for w in sorted_pops if w != None]

		sorted_times = sorted_times_2
		sorted_artists = sorted_artists_2
		sorted_pops = sorted_pops_2
		sorted_uris = sorted_uris_2


#	if not sorted_pops:
#			break

		uri_list.extend(uri_list_temp)
		time_list.extend(time_list_temp)

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

	print(playlist_id)
	populate_response = requests.post(url = populate_url, headers = populate_headers, data = json.dumps(populate_data))
	print(populate_response.status_code)
	return playlist_url

	
def search(track_list, journey_time):
	
	journey_time = journey_time*60000

	auth_code = authenticate()

	headers = {'Authorization' : "Bearer " + auth_code}
	
	url = 'https://api.spotify.com/v1/search'

	response_list = []

	for track in track_list:
	
		params = dict(
			q = str(track).replace(" ", "+"),
			type = "track",
			limit = '5')

	
		response = requests.get(url = url, headers = headers, params = params)
		for item in response.json()['tracks']['items']:
			response_list.append(item['id'])

	info = getTrackInfo(response_list, auth_code)

	playlist_url = createPlaylist(info, journey_time, auth_code)

	return playlist_url
