import io
import logging
import telepot
import requests
import xmltodict
from pprint import pprint as pp
from configparser import SafeConfigParser
from flask import Flask, request, abort, render_template, jsonify, send_file
import firebase_admin
from firebase_admin import credentials, db


from parse_ import Typhoon, Earthquake, debrisFlow, thunderstorm, railTransport, Tsunami, extremelyRain, ReservoirDis, bobe168, phone, workschoolQK
from utils import tformat, splitLine
##### configure #####
app = Flask(__name__)
parser = SafeConfigParser()
parser.read('config.txt')
owner = int(parser.get('owner', 'id'))
bot = telepot.Bot(parser.get('bot', 'token'))

resp = '<?xml version=\"1.0\" encoding=\"utf-8\" ?> <Data><Status>True</Status></Data>'
cred = firebase_admin.credentials.Certificate('token/firebase.json')
firebase_admin.initialize_app(cred, {'databaseURL': parser.get('bot', 'db')})
root = db.reference()

parseCase = {
	'颱風': Typhoon,
	'地震': Earthquake,
	'土石流': debrisFlow,
	'雷雨': thunderstorm,
	'鐵路事故': railTransport,
	'海嘯': Tsunami,
	'降雨': extremelyRain,
	'水庫放流': ReservoirDis,
	'道路封閉': bobe168,
	'市話通訊中斷': phone,
	'行動電話中斷': phone,
	'停班停課': workschoolQK
	}

##### flask http request #####
def fetch(url):
	r = requests.get(url)
	if r.status_code != 200:
		logging.critical("fetch data error")
		return 'Err'
	try:
		data = xmltodict.parse(r.text)
	except:
		logging.exception("xmltodict parse error")
		return 'Err'
	return data

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		data = request.data.decode('utf8')
		f = io.StringIO(data)
		try:
			data = xmltodict.parse(data)
			idf = data['alert']['identifier']
			if type(data['alert']['info']) == list:
				category = data['alert']['info'][0]['event']
			else:
				category = data['alert']['info']['event']
			bot.sendDocument(owner, (f'{category}.xml', f))
		except Exception as e:
			logging.exception("xmltodict parse error")
			bot.sendMessage(owner, f'{idf}\n{str(e)}')
			return resp
		try:
			if category in parseCase.keys():
				parseCase[category].parse(data)
		except Exception as e:
			bot.sendMessage(owner, '{e}'.format(str(e)))
		return resp

	return jsonify({'status': 'dafuq'})


@app.route('/typhoon', methods=['GET'])
def alert_typhoon():
	data = fetch('https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx?AlertType=5')
	parse = data['feed']['entry']
	for parse_ in parse:
		id = parse_['id']
		content = fetch(parse_['link']['@href'])
		dbId = db.reference('typhoon/').get()
		if id not in dbId.values():
			tt = Typhoon.alert(content)
			Typhoon.alert.parse(tt)
			new_data = root.child('typhoon').push(id)
		else:
			pass
	return jsonify({'status': 'dafuq'})


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
