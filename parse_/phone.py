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
chatIdList = config.get('channel', 'mobile').split(',')
owner = int(config.get('owner', 'id'))


def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 通訊中斷測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(parse_):
	'''
	發布單位：#國家通訊傳播委員會 {senderName}
	警報類型：#行動電話中斷 {event}
	警戒等級：🔴🔶 #紅色 {alertColor}

	停話區域：高雄市-橋頭區
	業者：亞太電信股份有限公司
	故障基地台數：1台
	#【NCC訊】停話區域：高雄市-橋頭區。業者：亞太電信股份有限公司 故障基地台數：1台。

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	# 警報類型
	headline = parse_['event']
	# 警報簡述
	desc = unicodedata.normalize('NFKC', parse_['description']).replace('【NCC訊】', '').replace('。', '\n').replace(' ', '\n')
	if type(parse_['parameter']) == list:
		for x in parse_['parameter']:
			# 警報顏色
			if x['valueName'] == 'alert_color':
				alertColor = {'橙色': '🔶 #橙色', '黃色': '⭐ #黃色',
							  '紅色': '🔴 #紅色', '綠色': '💚 #綠色'}[x['value']]
	else:
		alertColor = ''

	if alertColor:
		msg = f'發布單位：#{senderName}\n' \
			f'警報類型：#{headline}\n' \
			f'警戒等級：{alertColor}\n' \
			f'{desc}' \
			'\n' \
			f'警報發布時間：{effective}\n'

	else:
		if type(parse_['area']) == list:
			area = ''
			for y in parse_['area']:
				area += '	' + y['areaDesc'] + '\n'
		else:
			area = '	' + y['areaDesc'] + '\n'
		msg = f'發布單位：#{senderName}\n' \
			'警報類型：#全部區域已修復\n' \
			f'{desc}\n' \
			f'完修地點：\n{area}\n' \
			f'警報發布時間：{effective}\n'

	for chatId in chatIdList:
		while True:
			try:
				bot.sendMessage(
					int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
