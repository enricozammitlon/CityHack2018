#from app import app
from flask import render_template
from flask import Flask, request,flash,redirect
from TFL import getRoute
from spotifyQuerier import *
import nexmo
client = nexmo.Client(key='5882b5e8', secret='Ultimatum1616')
from forms import LoginForm

app = Flask(__name__)
global origin
origin=""
global destination
destination=""

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
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
	parts=route.split('to');
	origin=parts[0]
	destination=parts[1]
	sendBack()
	return 'ok'

@app.route('/calculate',methods=['GET', 'POST'])
def calculate():
	origin=request.form['origin']
	destination=request.form['destination']
	journeyDict = getRoute(origin, destination)
	link=search(journeyDict['Stations'], int(journeyDict['Time']))
	return redirect(link)

def sendBack():
	journeyDict = getRoute(origin, destination)
	link=search(journeyDict['Stations'], int(journeyDict['Time']))
	print(link)
	client.send_message({'from': '447418340203','to': request.args['msisdn'],'text': link})
	return 'ok part 2'
if __name__ == '__main__':
	app.run(host='139.59.184.20', port=80, debug=True)
