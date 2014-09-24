#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  trans_plugin.py

	
import urllib,httplib,re,simplejson
from string import replace
	
	
def handler_google_trans(type, source,parameters):
        if parameters == '':
                reply(type,source, u'hmmm?')
		return
        trlang = ['sq','af','ar','bg','ca','zh-CN','zh-TW','hr','cs','da',
		  'nl','en','et','tl','fi','fr','gl','de','el','iw',
		  'hi','hu','id','it','ja','ko','lv','lt','mt','no',
		  'pl','pt','ro','ru','sr','sk','sl','es','sv','th','tr','uk','vi']
	if parameters.strip()==u'list':
                if type == 'public':
                        reply(type,source,u'private')
                        msg = u'Accessible languages for translation:\n'
                        for tl in trlang: msg += tl+', '
                        msg = msg[:-2]
                reply('private',source,msg)
		return
	else:
		if parameters.count(' ') > 1:
			parameters = parameters.split(' ',2)
			if trlang.count(parameters[0]) and trlang.count(parameters[1]) and parameters[2] != '':
				query = urllib.urlencode({'q' : parameters[2].encode("utf-8"),'langpair':parameters[0]+'|'+parameters[1]})
				url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
				search_results = urllib.urlopen(url)
				json = simplejson.loads(search_results.read())
				msg = json['responseData']['translatedText']
			else: msg = u'Incorrect language or no text to translate. type tr list - for available languages'
		else: msg = u'Command format: tr code code text'
		reply(type, source, msg)

def handler_google_trans_autolang(type,source,parameters):
	if parameters == '':
		reply(type,source, u'And what do you mean?')
		return
	par=parameters.strip()
	rus = [u'а', u'б', u'в', u'г', u'д', u'е', u'ё', u'ж', u'з', u'и', u'й', u'к', u'л', u'м', u'н', u'о', u'п', u'р', u'с', u'т', u'у', u'ф', u'х', u'ц', u'ч', u'ш', u'щ', u'ъ', u'ь', u'ы', u'э', u'ю', u'я']
	eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	k = 0
	i = 0
	lang = 'not'
	while (k != 1):
		if (par[i] in rus):
			lang = 're'
			k = 1
		else:
			if (par[i] in eng):
				lang = 'er'
				k = 1
			else:
				i += 1
				if (i == len(par)-1):
					k = 1
	if lang == 'not':
		reply(type,source, u'Unable to determine the language!')
		return
	parameters = lang + ' ' + parameters
	stsp=string.split(parameters, ' ', 1)
	langpairs={'er': 'en ru', 're': 'ru en','ef': 'en fr','ed': 'en de', 'df': 'de fr','ei': 'en it', 'es': 'en sp', 'ep': 'en pt', 'ek': 'en ko', 'ej': 'en ja', 'ar': 'auto ru', 'ez': 'en id', 'ey': 'en pl', 'qe': 'af en', 'eq': 'en af', 'qr': 'af ru', 'rq': 'ru af', 'qa': 'af ar', 'aq': 'ar af', 'qz': 'af id', 'zq': 'id af', 'ye': 'pl en', 'ue': 'fa en', 'eu': 'en fa', 'fe': 'fr en', 'ze': 'id en', 'ea': 'en ar', 'ae': 'ar en', 'xe': 'ek en', 'ex': 'en ek', 'zx': 'id ek', 'he': 'hi en', 'eh': 'en hi', 'eg': 'en el', 'ge': 'el en', 'ew': 'en iw', 'we': 'iw en', 'zr': 'id ru', 'za': 'id ar', 'rj': 'ru ja', 'ar': 'ar ru', 'ra': 'ru ar', 'ec': 'en zh-CN', 'ce': 'zh-CN en', 'rc': 'ru zh-CN', 'ac': 'ar zh-CN', 'zc': 'id zh-CN', 'cz': 'zh-CN id', 'el': 'en tl', 'le': 'tl en', 'em': 'en mt', 'me': 'mt en', 'et': 'en th', 'te': 'th en', 'se': 'sp en'}
	if langpairs.has_key(stsp[0]):
		pair=langpairs[stsp[0]]
		pair=string.split(pair, ' ', 1)
		query = urllib.urlencode({'q' : stsp[1].encode("utf-8"),'langpair':pair[0]+'|'+pair[1]})
		url = u'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
		search_results = urllib.urlopen(url)
		json = simplejson.loads(search_results.read())
		msg = json['responseData']['translatedText']
		reply(type,source,msg)
	else:
		reply(type,source,u'what is that language?')
		

register_command_handler(handler_google_trans, 'tr', ['info','all'], 0, 'Translates a phrase in one language into another. More - write, tr list. " ',' Tr <language code> <language code> <phrase> ', [' tr en ru hello',' tr ru en привет'])
register_command_handler(handler_google_trans_autolang, '!', ['info','all', 'new'], 0, 'auto translation from english to russian and vice versa, ', '! <phrase>', ['! hello', '! привет'])
