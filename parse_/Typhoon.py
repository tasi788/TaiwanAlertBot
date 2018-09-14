import re
import telepot
import logging
import requests
import xmltodict
import unicodedata
from time import strftime
from pyquery import PyQuery as pq
from utils import tformat, splitLine
from configparser import SafeConfigParser

from pprint import pprint as pp

config = SafeConfigParser()
config.read('config.txt')
bot = telepot.Bot(config.get('bot', 'token'))
chatIdList = config.get('channel', 'typhoon').split(',')
owner = int(config.get('owner', 'id'))

def parse(content):
	parse = content['alert']['info']
	id = content['alert']['identifier']
	status = content['alert']['status']
	nowY = strftime('%Y')

	if status.lower() != 'actual':
		logging.warning(f'{id} 颱風測試檔案')
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
	警報等級：🔴 #紅色
	警報類型：#海上陸上颱風警報

	瑪莉亞(MARIA) 強烈颱風
	------------------------
	颱風動態：根據最新資料顯示，第8號颱風過去3小時強度稍減弱，目前中心在宜蘭東方810公里之海面上，向
	西北西移動。其暴風圈正快速向臺灣東方海面接近，對臺灣北部海面、東北部海面、東南部海面及
	臺灣海峽北部將構成威脅。

	警戒區域及事項：陸上：新北、基隆、臺北、宜蘭應嚴加戒備並防強風豪雨。
	海上：臺灣北部海面、臺灣東北部海面、臺灣東南部海面(含蘭嶼、綠島)及臺灣海峽北部航行及作
	業船隻應嚴加戒備。

	注意事項：臺灣北部、西南部、東半部濱海地區及綠島、蘭嶼、恆春半島、馬祖已有長浪出現，請避免前
	 往海邊活動。
	明(10日)上午起至11日清晨臺東及花蓮地區將有焚風發生的機率，請注意。
	影響範圍：臺灣北部海面、臺灣東北部海面、臺灣東南部海面、臺灣海峽北部、基隆、臺北、新北、宜蘭。
	------------------------

	備註
	相關詳細颱風動態資訊請上氣象局網站

	警報發布時間：2018年07月09日 23:30
	========================================
	發布單位：#中央氣象局
	警報類型：#解除颱風警報

	瑪莉亞(MARIA) 強烈颱風
	------------------------
	颱風動態：根據最新資料顯示，第8號颱風已於今(11)日14時減弱為輕度颱風，過去3小時強度持續減弱，暴風 圈亦縮小，目前中心在馬祖西北西方之陸地上，繼續向西北西移動，馬祖已脫離其暴風圈。預計此 颱風強度有持續減弱且暴風圈有縮小的趨勢。
	警戒區域及事項：臺灣北部海面、臺灣東北部海面及臺灣東南部海面(含蘭嶼、綠島)航行及作業船隻 應嚴加戒備。
	注意事項：*颱風外圍環流影響，臺灣各沿海地區及馬祖風浪仍強，前往海邊活動請注意安全。 *9日0時至11日14時出現較大累積雨量如下：臺北市油坑407毫米、新竹縣白蘭307毫米、臺中市稍 來282毫米、苗栗縣鳳美273毫米、新北市信賢派出所260毫米、桃園市高坡國小248毫米、宜蘭縣福 山植物園211毫米。出現較大陣風地區如下：彭佳嶼16級、新北市鼻頭角14級、連江縣東引13級、 蘭嶼11級、臺北市大直10級。
	影響範圍：基隆市、台北市、新北市。

	*備註*
	相關詳細颱風動態資訊請上[氣象局網站](https://www.cwb.gov.tw/V7/prevent/warning.htm)

	警報解除發布時間：2018年8月27日 8:30 AM
	'''
	effective = tformat(parse_['effective'])
	senderName = parse_['senderName']
	category = parse_['event']
	# 警報類型
	headline = parse_['headline']
	# 區域
	if type(parse_['area']) == list:
		area = ''
		for y in parse_['area']:
			if y['areaDesc'] == parse_['area'][-1]['areaDesc']:
				area += y['areaDesc'] + '。'
			else:
				area += y['areaDesc'] + '、'
	else:
		area = parse_['area']['areaDesc']
	# 解除警報處理
	if headline == '解除颱風警報':
		try:
			for x in parse_['description'].split('['):
				if x[:4] == '颱風動態':
					data_ = x.replace('\n', '').replace(']', '：')
					typData = unicodedata.normalize('NFKC', data_)
			num_ = re.findall('第\d+號颱風', typData)[0]
			num = re.findall('\d+', num_)[0]
			if len(num) == 1:
				tyNum_ = f'{nowY}0{num}'
			else:
				tyNum_ = f'{nowY}{num}'
			url = 'http://rdc28.cwb.gov.tw/TDB/ctrl_typhoon_list/get_typhoon_list_table'
			data = {'year': nowY, 'model': 'all'}
			req = requests.post(url, data=data)
			cParse = pq(req.text)('tr')
			for x in range(2, len(cParse)):
				tyNum = cParse.eq(x)('td').eq(1).text()
				twName = cParse.eq(x)('td').eq(2).text()
				enName = cParse.eq(x)('td').eq(3).text()
				if tyNum == tyNum_:
					typhoon_ = f'{twName}({enName})'
			msg = f'發布單位：#{senderName}\n' \
				f'警報類型：#{headline}\n' \
				'\n' \
				f'{typhoon_}\n' \
				f'{splitLine(typhoon_)}\n' \
				f'{typData}\n' \
				'\n' \
				f'影響範圍：{area}\n' \
				f'{splitLine(typhoon_)}\n' \
				'\n' \
				'*備註*\n' \
				'相關詳細颱風動態資訊請上<a href="https://www.cwb.gov.tw/V7/prevent/warning.htm/">氣象局網站</a>\n' \
				'\n' \
				f'警報發布時間：{effective}\n'
			print('================\n', msg, '\n=================')
		except Exception as e:
			logging.exception(e)
			bot.sendMessage(owner, str(e), parse_mode='html')
	else:
		securityLevel = {'海上陸上颱風警報': '🔴 #紅色',
						 '海上颱風警報': '🔶 #橙色'}[headline]
		# 颱風名稱 強度
		for x in parse_['description']['typhoon-info']['section']:
			if x['@title'] == '颱風資訊':
				enName = x['typhoon_name']
				twName = x['cwb_typhoon_name']
				for y in x['analysis']['scale']:
					if y['@lang'] == 'zh-TW':
						typStrong = y['#text']
		typhoon_ = f'{twName}({enName}) {typStrong}'
		# 颱風動態
		for desc in parse_['description']['section']:
			if desc['@title'] == '颱風動態':
				descNews = desc['#text'].replace(
					'\n', '').replace('。', '。\n')
			elif desc['@title'] == '警戒區域及事項':
				descAlert = desc['#text'].replace(
					'\n', '').replace('。', '。\n')
			elif desc['@title'] == '注意事項':
				descInstru = desc['#text'].replace(
					'\n', '').replace('。', '。\n')

		msg = f'發布單位：#{senderName}\n' \
			f'警報等級：{securityLevel}\n' \
			f'警報類型：#{headline}\n' \
			'\n' \
			f'{typhoon_}\n' \
			f'{splitLine(typhoon_)}\n' \
			f'颱風動態：{descNews}\n' \
			'\n' \
			f'警戒區域及事項：{descAlert}\n' \
			'\n' \
			f'注意事項：{descInstru}\n' \
			'\n' \
			f'影響範圍：{area}\n' \
			f'{splitLine(typhoon_)}\n' \
			'\n' \
			'*備註*\n' \
			'相關詳細颱風動態資訊請上<a href="https://www.cwb.gov.tw/V7/prevent/warning.htm/">氣象局網站</a>\n' \
			'\n' \
			f'警報發布時間：{effective}\n'
	for chatId in chatIdList:
		while True:
			try:
				#print(msg)
				bot.sendMessage(
					int(chatId), msg, parse_mode='html', disable_web_page_preview=True)
				break
			except Exception as e:
				logging.exception(e)
				pass
