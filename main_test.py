import requests
import xmltodict
from parse_ import workschoolQK

url = 'https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx?AlertType=33'

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

data = fetch(url)
parse = data['feed']['entry']
for parse_ in parse:
	content = fetch(parse_['link']['@href'])
	try:
		workschoolQK.parse(content)
	except:
		print(parse_['link']['@href'])
