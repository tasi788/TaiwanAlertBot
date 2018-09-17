import telepot
import logging
import requests
import xmltodict
import unicodedata
import re
from time import strftime
from utils import tformat
from configparser import SafeConfigParser

from pprint import pprint as pp

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
		logging.warning(f'{id} 雷雨測試檔案')
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
	警報類型：#雷雨即時訊息 {headline}
	警戒等級：🔴🔶 #紅色 #豪雨 {alertColor} {severity_level}
	警報簡述：午後對流發展旺盛，今（２）日屏東地區及嘉義、高雄山區有局部大雨或豪雨發生的機率，其他各地山區有局部大雨發生的機率，請注意瞬間大雨、雷擊及強陣風。 {desc}

	影響區域：
					屏東縣新埤鄉 {area}
					屏東縣竹田鄉

	*備註*
	相關詳細強降雨警報請上[氣象局網站](https://www.cwb.gov.tw/V7/prevent/warning.htm)

	警報發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	# 警報類型
	headline = parse_['headline']
	# 警報簡述
	desc = unicodedata.normalize('NFKC', parse_['description'])
	#desc = re.sub(r"([0-9]+)( *年)","2018"+r"\2",d)
	desc = re.sub(r"^([0-9]{3}) *年 *", "", desc)
	if type(parse_['parameter']) == list:
		for x in parse_['parameter']:
			# 警報顏色
			if x['valueName'] == 'alert_color':
				alertColor = {'橙色': '🔶 #橙色', '黃色': '⭐ #黃色',
							'紅色': '🔴 #紅色', '綠色': '💚 #綠色'}[x['value']]
	else:
		alertColor = ''
	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			area += '	' + y['areaDesc'] + '\n'
	else:
		area = '	' + parse_['area']['areaDesc'] + '\n'

	msg = f'發布單位：#{senderName}\n' \
		f'警報類型：#{headline}\n' \
		f'警戒等級：{alertColor} #豪雨\n' \
		f'警報簡述：{desc}\n' \
		'\n' \
		f'影響區域：\n{area}\n' \
		'\n' \
		'*備註*\n' \
		f'相關詳細雷雨警報請上 <a href="https://www.cwb.gov.tw/V7/prevent/warning.htm">氣象局網站</a>\n' \
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
