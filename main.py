from TFL import getRoute
from spotifyQuerier import *

origin = input("Origin: ")
destination = input("Destination: ")

journeyDict = getRoute(origin, destination)

print(search(journeyDict['Stations'], int(journeyDict['Time'])))
