import telepot
import logging
import requests
import xmltodict
from utils import tformat
from pprint import pprint as pp
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.txt')
bot = telepot.Bot(config.get('bot', 'token'))
chatIdList = config.get('channel', 'thunderstorm').split(',')
owner = int(config.get('owner', 'id'))


def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 台鐵測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(parse_):
	'''
	發布單位：#臺灣鐵路管理局
	警報類型：#鐵路事故 {event}
	警戒等級：🔴🔶 #紅色 #停駛 {alert_color} {severity_level}
	警報簡述：臺鐵台鐵局因應南部豪雨8月23日列車行車資訊停駛 {headline}

	影響路線：
					台北 ↔️ 板橋 {area}
					板橋 ↔️ 桃園

	*備註*
	請上臺鐵網站查詢最新[營運狀態](http://www.railway.gov.tw/tw/index.html)

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	headline = parse_['headline']
	category = parse_['event']
	for x in parse_['parameter']:
		# 警報顏色
		if x['valueName'] == 'alert_color':
			alertColor = {'黃色': '🔶 #黃色', '紅色': '🔴 #紅色',
						  '綠色': '💚 #綠色'}[x['value']]
		# 營運狀況
		elif x['valueName'] == 'severity_level':
			if x['value'] not in ['停駛', '營運異常']:
				securityLevel = ''
			else:
				securityLevel = '#' + x['value']

	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			area += '	' + y['areaDesc'].replace('-', ' ↔️ ') + '\n'
	else:
		area = '	' + parse_['area']['areaDesc'].replace('-', ' ↔️ ') + '\n'
	msg = f'發布單位：#{senderName}\n' \
		f'警報類型：#{category}\n' \
		f'警戒等級：{alertColor} {securityLevel}\n' \
		f'警報簡述：{headline}\n' \
		'\n' \
		f'影響路線：\n{area}\n' \
		'\n' \
		'*備註*\n' \
		f'請上臺鐵網站查詢最新<a href="http://www.railway.gov.tw/tw/index.html">營運狀態</a>\n' \
		'\n' \
		f'警報發布時間：{effective}\n'

	for chatId in chatIdList:
		while True:
			try:
				print(msg)
				#bot.sendMessage(
				#	int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
