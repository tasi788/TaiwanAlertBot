import tra, thsr

def parse(content):
	'''
	~ an adapter for rail ~
	'''
	id = content['alert']['identifier']
	if 'thsrc.com.tw' in id:
		thsr.parse(content)
	else:
		tra.parse(content)
