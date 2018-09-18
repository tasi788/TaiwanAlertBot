import re
import telepot
import logging
import requests
import xmltodict
import unicodedata
from time import strftime
from utils import tformat
from pprint import pprint as pp
from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.txt')
bot = telepot.Bot(config.get('bot', 'token'))
chatIdList = config.get('channel', 'bobe168').split(',')
owner = int(config.get('owner', 'id'))


def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 道路封閉測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(parse_):
	'''
	發布單位：#交通部公路總 {senderName}
	警報類型：#道路封閉 {event}
	警戒等級：🔴🔶 #紅色 #災害性封閉 {alertColor} {RoadClose_type}
	警報簡述：台東縣 海端鄉 台20線159K+000~159K+000，因 邊坡坍方災害封閉。 災害發生時間：2018/9/12 上午 10:10:00
	預計搶通時間：2018/9/12 下午 01:00:00

	影響區域：
		台20線159K+000~159K+000


	*備註*
	相關詳細道路封閉警報請上[交通部公路防救災資訊系統網站](https://bobe168.tw/)

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	# 警報類型
	headline = parse_['event']
	# 警報簡述
	desc = unicodedata.normalize('NFKC', parse_['description']).replace(';', '\n')
	if type(parse_['parameter']) == list:
		for x in parse_['parameter']:
			# 警報顏色
			if x['valueName'] == 'alert_color':
				alertColor = {'橙色': '🔶 #橙色', '黃色': '⭐ #黃色',
							  '紅色': '🔴 #紅色', '綠色': '💚 #綠色'}[x['value']]
			elif x['valueName'] == 'RoadClose_type':
				alertType = x['value']
	else:
		alertColor = ''
	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			area += '	' + y['areaDesc'] + '\n'
	else:
		area = '	' + parse_['area']['areaDesc']
		lat, lon = parse_['area']['circle'].split(' ')[0].split(',')
	if alertColor == '💚 #綠色':
		msg = f'發布單位：#{senderName}\n' \
			f'警戒等級：{alertColor}\n' \
			f'警報簡述：{desc}\n' \
			'*備註*\n' \
			'相關詳細道路封閉警報請上 <a href="https://bobe168.tw/">交通部公路防救災資訊系統網站</a>\n' \
			'\n' \
			f'警報發布時間：{effective}\n'
	else:
		msg = f'發布單位：#{senderName}\n' \
			f'警報類型：#{headline}\n' \
			f'警戒等級：{alertColor} #{alertType}\n' \
			f'警報簡述：{desc}\n' \
			'\n' \
			f'影響區域：\n{area}\n' \
			'\n' \
			'*備註*\n' \
			'相關詳細道路封閉警報請上 <a href="https://bobe168.tw/">交通部公路防救災資訊系統網站</a>\n' \
			'\n' \
			f'警報發布時間：{effective}\n'

	for chatId in chatIdList:
		while True:
			try:
				if lat:
					bot.sendVenue(
						chatId,
						float(lat),
						float(lon),
						'道路封閉座標',
						f'{lat} {lon}',
						disable_notification=True)
				bot.sendMessage(
					int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
