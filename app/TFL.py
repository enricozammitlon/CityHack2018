#--------------------------------------------------------------------
# Transport For London API caller by Enrico Zammit Lonardelli
# enrico.zammitl@gmail.com - enricozl.me
#--------------------------------------------------------------------

import requests
import json

def getRoute(origin,destination):
    exceptions = {'Paddington':'1000174', 'Waterloo':'1000254', 'Euston':'1000077'}
    if origin not in exceptions:
        origin=origin+" Underground Station"
    else:
        origin = exceptions[origin]

    if destination not in exceptions:
        destination=destination+" Underground Station"
    else:
        destination = exceptions[destination]
    KEY=""
    fp=open('keys.txt', 'r')
    for line in fp:
        KEY=str(line)
    request="https://api.tfl.gov.uk/Journey/JourneyResults/"+origin+"/to/"+destination+"?mode=tube"+str(KEY)
    requestedData = requests.get(request)
    jasonData = requestedData.json()
    journeysDict=[origin]
    counter=0
    time=0

    time=jasonData['journeys'][0]['duration']
    for b in jasonData['journeys'][0]['legs']:
        for c in b['path']['stopPoints']:
            journeysDict.append(c['name'])
            counter+=1
    journeysDict=sorted(set(journeysDict))
    totalData={"Time":time,"Stations":journeysDict}
    with open('out.json', 'w') as fp:
        fp.write(json.dumps(jasonData, indent=4, sort_keys=True))
    return totalData
