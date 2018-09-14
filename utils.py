from dateutil.parser import parse as dateParse
from PIL import Image,ImageDraw,ImageFont
import telepot

def tformat(rawTime):
	# 2018年8月23日 5:30 PM
	tformat_ = '%Y/%m/%d/ %H:%M'
	parse = dateParse(rawTime).strftime(tformat_)
	parse_ = parse.split('/')
	tmp = ''
	for x, y in zip(['年', '月', '日', ''], parse_):
		tmp += y + x
	return tmp

def splitLine(world):
	im = Image.new('RGB', (60, 30), color = 'red')
	draw = ImageDraw.Draw(im)
	msg = f'{world}'.encode('utf-8')
	w,h = draw.textsize(msg)
	return '-'*round(w/6)+'-'
