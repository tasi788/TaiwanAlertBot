import io
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
chatIdList = config.get('channel', 'earthquake').split(',')
owner = int(config.get('owner', 'id'))

def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 地震測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)

def msgfromat(parse_):
	'''
	發布單位：#中央氣象局
	警報類型：#地震報告
	發生地點：花蓮縣秀林鄉#EventLocationName
	地震強度：芮氏規模4.3
	地震深度：17.7公里 #EventDepth
	警報簡述：09/03 13:59花蓮縣秀林鄉發生規模4.3有感地震，最大震度花蓮縣銅門5級。

	各地最大震度：
		5級 花蓮縣
		3級 南投縣
		3級 臺中市

	*備註*
	相關詳細地震資訊請上[地震測報中心](https://scweb.cwb.gov.tw/GraphicContent.aspx?ItemId=49&fileString=2018090313594943117)

	警報發布時間：2018年8月27日 8:30 AM
	'''
	onset = tformat(parse_['onset'])
	senderName = parse_['senderName']
	category = parse_['event']
	quakelocationlevel = ''
	#地震簡述
	desc = parse_['description']
	#網站
	site = parse_['web']
	#各地最大震度
	for y in parse_['area']:
		if 'circle' in y:
			area = y['areaDesc']
	#地震地點 地震強度 各地最大震度
	for x in parse_['parameter']:
		if x['valueName'] == 'EventLocationName':
			eventLocation = x['value']
		elif x['valueName'] == 'EventMagnitudeDescription':
			quakelevel = x['value']
		elif x['valueName'] == 'LocalMaxIntensity':
			tmp = x['value'].replace('"', ' ').split(';', 2)
			tmp.pop(2)
			d = 0
			quakelocationlevel += f'	{tmp[0]} {tmp[1]}\n'
		elif x['valueName'] == 'EventDepth':
			depth = x['value']
		elif x['valueName'] == 'EventPublisher':
			eventpublisher = x['value']
	#圖
	for pics in parse_['resource']:
		if pics['resourceDesc'] == '地震報告圖':
			pic = pics['uri']
			pic_ = requests.get(pic.replace('.gif', '_H.png'), stream=True)
			if pic_.status_code == 200:
				pic_.decode_content = True
				pic = io.BytesIO(pic_.content)
				#with open('earthquake.png', 'wb') as fd:
				#	for chunk in pic_.iter_content(chunk_size=128):
				#		fd.write(chunk)
				#pic = open('earthquake.png', 'rb')
	msg = f'發布單位：#{senderName}\n' \
		f'地震資料來源：{eventpublisher}\n' \
		f'警報類型：#{category}\n' \
		f'震央位置：{eventLocation}\n' \
		f'地震強度：{quakelevel}\n' \
		f'地震深度：{depth}\n' \
		f'警報簡述：{desc}\n' \
		'\n' \
		f'各地最大震度：\n{quakelocationlevel}\n' \
		'\n' \
		'*備註*\n' \
		f'相關詳細地震資訊請上<a href="{site}">地震測報中心</a>\n' \
		'\n' \
		f'警報發布時間：{onset}\n'
	for chatId in chatIdList:
		while True:
			try:
				bot.sendPhoto(
					int(chatId), pic
				)
				bot.sendMessage(
					int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
