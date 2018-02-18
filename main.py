from ./TFL/TFL.py import *
from ./Spotify/spotifyQuerier.py import *

origin = input("Origin: ")
destination = input("Destination: ")

journeyDict = getRoute(origin, destination)

print(search(journeyDict['Stations'], journeyDict['Time']))
