#from app import app
#from flask import render_template
from flask import Flask, request
from TFL import getRoute
from spotifyQuerier import *
import nexmo
client = nexmo.Client(key='5882b5e8', secret='Ultimatum1616')

app = Flask(__name__)
global origin
origin=""
global destination
destination=""

@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')
"""
@app.route('/delivery-receipt', methods=["POST"])
def aboutme():
	return ("")
"""
@app.route('/inbound-sms', methods=["GET"])
def inbound_sms():
	global origin
	global destination
	route=request.args['text']
	parts=route.split(' ');
	origin=parts[0]
	destination=parts[2]
	sendBack()
	return 'ok'

def sendBack():
	journeyDict = getRoute(origin, destination)
	link=search(journeyDict['Stations'], int(journeyDict['Time']))
	print(link)
	client.send_message({'from': 'TubeAmp','to': request.args['msisdn'],'text': link})
	return 'ok part 2'

app.run(host='139.59.184.20', port=80, debug=True)
