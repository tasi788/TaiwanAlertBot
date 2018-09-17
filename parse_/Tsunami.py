import telepot
import logging
import requests
import xmltodict
import unicodedata
from utils import tformat

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
		logging.warning(f'{id} 海嘯測試檔案')
		return
	else:
		if type(parse) == list:
			for x in parse:
				msgfromat(x)
		else:
			msgfromat(parse)


def msgfromat(parse_):
	'''
	senf
	發布單位：#中央氣象局
	地震資料來源：#中央氣象局
	警報類型：#海嘯警報 {healine}
	警戒等級：🔴🔶 #紅色
	發生地點：臺灣東部海域 {EventLocationName}
	地震強度：7.5
	地震深度：20.0公里 #EventDepth
	警報簡述：（例行測試）２０１５年０９月２１日０９時２１分（臺灣時間），在東經１２２﹒１９度、北緯２４﹒１４度，發生規模７﹒５地震。有可能引發海嘯，請沿海地區提高警覺嚴加防範。

	各分區預估波高等級：
			東南沿海地區 小於1公尺
			北部沿海地區 小於1公尺

	各分區預估海嘯到時：
			東南沿海地區 2018年8月27日 8:30 AM
			北部沿海地區 2018年8月27日 8:30 AM

	*備註*
	相關詳細海嘯資訊請上[地震測報中心](https://scweb.cwb.gov.tw/GraphicContent.aspx?ItemId=49&fileString=2018090313594943117)

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	headline = parse_['headline']
	predictTime, predictWave = '', ''
	# 地震簡述
	desc = unicodedata.normalize('NFKC', parse_['description'])
	# 網站
	site = parse_['web']
	for x in parse_['parameter']:
		# 地震地點
		if x['valueName'] == 'EventLocationName':
			eventLocation = x['value']
		# 警報顏色
		elif x['valueName'] == 'alert_color':
			securityLevel = {'橙色': '🔶 #橙色', '黃色': '⭐ #黃色',
							 '紅色': '🔴 #紅色', '綠色': '💚 #綠色'}[x['value']]
		# 地震規模
		elif x['valueName'] == 'EventMagnitude':
			quakelevel = x['value']
		# 震源深度
		elif x['valueName'] == 'EventDepth':
			depth = x['value']
		# 震央座標
		elif x['valueName'] == 'EventLatLon':
			lat, lon = x['value'].split(' ')[0].split(',')
		# 資料來源
		elif x['valueName'] == 'EventPublisher':
			eventpublisher = x['value']
		# 預測到達時間
		elif x['valueName'] == 'PredictedArrivalTime':
			tmp = x['value'].replace('"', ' ').split(';', 2)
			tmp.pop(2)
			d = 0
			predictTime += f'	{tmp[0]} {tformat(tmp[1])}\n'
		# 各分區預估波高等級
		elif x['valueName'] == 'PredictedWaveHeight':
			tmp = x['value'].replace('"', ' ').split(';', 2)
			tmp.pop(2)
			d = 0
			predictWave += f'	{tmp[0]} {tmp[1]}\n'
	msg = f'發布單位：#{senderName}\n' \
		f'地震資料來源：#{eventpublisher}\n' \
		f'警報類型：#{headline}\n' \
		f'警戒等級：{securityLevel}\n' \
		f'震央位置：{eventLocation}\n' \
		f'地震強度：{quakelevel}\n' \
		f'地震深度：{depth}\n' \
		f'警報簡述：{desc}\n' \
		'\n' \
		f'各分區預估波高等級：\n{predictWave}\n' \
		'\n' \
		f'各分區預估海嘯到時：\n{predictTime}\n' \
		'\n' \
		'*備註*\n' \
		f'相關詳細海嘯資訊請上<a href="{site}">地震測報中心</a>\n' \
		'\n' \
		f'警報發布時間：{effective}\n'
	for chatId in chatIdList:
		while True:
			try:
				# print(msg)
				bot.sendVenue(
					chatId,
					float(lat),
					float(lon),
					'震源座標',
					f'{lat} {lon}',
					disable_notification=True)
				bot.sendMessage(
					chatId, msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
