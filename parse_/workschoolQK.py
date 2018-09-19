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
chatIdList = config.get('channel', 'workschoolQK').split(',')
owner = int(config.get('owner', 'id'))


def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 停班課通知測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(parse_):
	'''
	發布單位：#行政院人事行政總處 {senderName}
	警報類型：#停班課通知 {event}
	警戒等級：🔴🔶 #紅色 {alertColor}

	彰化縣 8/23晚上停止上班、停止上課
	行政院人事行政總處
	如有任何問題請撥04-7531431。

	[停班停課通知]彰化縣:8/23晚上停止上班、停止上課。行政院人事行政總處。如有任何問題請撥04-7531431。
	*備註*
	適用範圍為各級政府機關及公、私立學校； 至交通運輸、警察、消防、海岸巡防、醫療、關務等業務性質特殊機關（構），為全年無休服務民眾， 且應實施輪班、輪休制度，如遇天然災害發生時，其尚無停止上班之適用。

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	# 警報類型
	headline = parse_['event']
	# 警報簡述
	desc = unicodedata.normalize('NFKC', parse_['description']).split(']', 1)[1].replace('。', '\n')
	instru = parse_['instruction'].replace('\n', '')
	if type(parse_['parameter']) == list:
		for x in parse_['parameter']:
			# 警報顏色
			if x['valueName'] == 'alert_color':
				alertColor = {'橙色': '🔶 #橙色', '黃色': '⭐ #黃色',
							  '紅色': '🔴 #紅色', '綠色': '💚 #綠色',
							  '紫色': '😈 #紫色', '黑色': '⚫ #黑色'}[x['value']]
	else:
		alertColor = ''
	msg = f'發布單位：#{senderName}\n' \
		f'警報類型：#{headline}\n' \
		f'警戒等級：{alertColor}\n' \
		'\n' \
		f'{desc}\n' \
		'*備註*\n' \
		f'{instru}\n' \
		'\n' \
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
