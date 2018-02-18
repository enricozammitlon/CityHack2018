import requests
import json

def getRoute(origin,destination):
    origin=origin" Underground Station"
    destination=destination+" Underground Station"
    KEY=""
    fp=open('keys.txt', 'r')
    for line in fp:
        KEY=str(line)
    print(KEY)
    request="https://api.tfl.gov.uk/Journey/JourneyResults/"+origin+"/to/"+destination+str(KEY)
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

origin=input("From:\n")+" Underground Station"
destination=input("To:\n")+" Underground Station"

print(origin)
print(getRoute(origin,destination))
