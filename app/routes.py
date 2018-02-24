#from app import app
from flask import render_template
from flask import Flask, request,flash,redirect
from TFL import getRoute
from spotifyQuerier import *
import nexmo
from forms import LoginForm

with open('/var/www/html/tubeamp.me/app/.htnexmo.txt', 'r') as f:
	content = f.readlines()
        key = content[0]
        secret = content[1]
	client = nexmo.Client(key = key, secret = secret)

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
	app.run(host='127.0.0.1', port=80, debug=True)
