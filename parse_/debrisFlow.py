import telepot
import logging
import requests
import xmltodict
from time import strftime
from utils import tformat
from configparser import SafeConfigParser
from pprint import pprint as pp


config = SafeConfigParser()
config.read('config.txt')
bot = telepot.Bot(config.get('bot', 'token'))
chatIdList = config.get('channel', 'debrisFlow').split(',')
owner = int(config.get('owner', 'id'))

def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']
	nowY = strftime('%Y')

	if status.lower() != 'actual':
		logging.warning(f'{id} 土石流測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)

def msgfromat(parse_):
	# 土石流
	'''
	發布單位：#農委會水土保持局
	警報等級：#紅色
	警報類型：#土石流 #土石流紅色警戒
	警報簡述：依據中央氣象局風雨資料研判：計20條土石流潛勢溪流達紅色警戒。
	注意事項：請配合鄉(鎮、市、區)公所及當地警消單位指示，儘早撤離或前往避難處所避難，並與當地避難處所保持聯繫，有關當地避難處所相關聯絡資訊，請詳土石流疏散避難圖。
	影響範圍：臺南市柳營區

	*備註*
	[相關詳細土石流警戒資訊請上土石流防災資訊網](http://246.swcb.gov.tw)

	警報發布時間：2018年8月27日 8:30 AM
	警報解除時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	expires = tformat(parse_['expires'])
	senderName = parse_['senderName']
	category = parse_['event']
	try:
		desc = parse_['description'].split('(相關詳細土石流警戒資訊請上土石流防災資訊網')[0]
	except:
		desc = parse_['description']
	securityLevel = {'Extreme': '🔴 #紅色 #土石流紅色警戒',
					 'Moderate': '🔶 #黃色 #土石流黃色警戒'}[parse_['severity']]
	instru = parse_['instruction']
	site = parse_['web']
	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			if y['areaDesc'] == parse_['area'][-1]['areaDesc']:
				area += y['areaDesc'] + '。'
			else:
				area += y['areaDesc'] + '、'
	else:
		area = parse_['area']['areaDesc']
	msg = f'發布單位：#{senderName}\n' \
		f'警報等級：{securityLevel}\n' \
		f'警報類型：#{category}\n' \
		f'警報簡述：{desc}\n' \
		f'注意事項：{instru}\n' \
		f'影響範圍：{area}\n' \
		'\n' \
		'*備註*\n' \
		f'相關詳細土石流警戒資訊請上<a href="{site}">土石流防災資訊網</a>\n' \
		'\n' \
		f'警報發布時間：{effective}\n' \
		f'警報解除時間：{expires}'
	for chatId in chatIdList:
		while True:
			try:
				bot.sendMessage(
					int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
