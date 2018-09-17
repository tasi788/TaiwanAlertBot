import telepot
import logging
import requests
import xmltodict
from utils import tformat
from pprint import pprint as pp


config = SafeConfigParser()
config.read('config.txt')
bot = telepot.Bot(config.get('bot', 'token'))
chatIdList = config.get('channel', 'earthquake').split(',')
owner = int(config.get('owner', 'id'))


def parse(self):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']

	if status.lower() != 'actual':
		logging.warning(f'{id} 高鐵測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(self, parse_):
	'''
	發布單位：#台灣高速鐵路股份有限公司
	警報類型：#鐵路事故 {event}
	警戒等級：🔴🔶 #紅色 #停駛 {alert_color} {severity_level}
	警報簡述：台灣高鐵部份區間延誤 {headline}
	因受板橋車站道岔訊號異常影響，導致部分列車延誤，本公司已派員處理中，造成不便敬請見諒。 {desc}

	影響路線：
			台北 ↔️ 板橋 {area}
			板橋 ↔️ 桃園

	*備註*
	請至台灣高鐵官方網站查詢最新[營運狀態](http://www.thsrc.com.tw/tw/Operation)

	警報發布時間：2018年8月27日 8:30 AM
	警報解除時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	headline = parse_['headline']
	category = parse_['event']
	# 災害簡述
	desc = parse_['description']
	# 網站
	site = parse_['web']
	for x in parse_['parameter']:
		# 警報顏色
		if x['valueName'] == 'alert_color':
			alertColor = {'黃色': '🔶 #黃色', '紅色': '🔴 #紅色',
						  '綠色': '💚 #綠色'}[x['value']]
		# 營運狀況
		elif x['valueName'] == 'severity_level':
			securityLevel = x['value']

	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			area += '	' + y['areaDesc'].replace('~', ' ↔️ ') + '\n'
	else:
		#area = '	' + y['areaDesc'].replace('~', ' ↔️ ')
		area = '	' + y['areaDesc'].replace('~', ' ↔️ ') + '\n'

	msg = f'發布單位：#{senderName}\n' \
		f'警報類型：#{category}\n' \
		f'警戒等級：{alertColor} #{securityLevel}\n' \
		f'警報簡述：#{headline}\n' \
		f'{desc}\n' \
		'\n' \
		f'影響路線：\n{area}\n' \
		'\n' \
		'*備註*\n' \
		f'請至台灣高鐵官方網站查詢最新<a href="http://www.thsrc.com.tw/tw/Operation">營運狀態</a>\n' \
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
