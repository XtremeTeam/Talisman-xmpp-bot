#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  trans_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Parts of code Copyright © Krishna Pattabiraman (PyTrans project) <http://code.google.com/p/pytrans/>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
	
import urllib
import httplib
import re

def google_translate(from_lang, to_lang, text):
	params = urllib.urlencode({"langpair":"%s|%s" %(from_lang, to_lang), "text":text,"ie":"UTF8", "oe":"UTF8"})
	conn = httplib.HTTPConnection("translate.google.com")
	conn.request("POST", "/translate_t", params)

	resp = conn.getresponse()
	s = resp.read()
	conn.close()

	match = re.compile('<div id=result_box.*?>(.*?)</div>',re.DOTALL).search(s)
	data = match.groups()[0]
	return unicode(data, "utf-8").strip()
	
	
def handler_google_trans(type,source,parameters):
	if parameters.strip()==u'языки':
		if type == 'public':
			reply(type,source,u'ушли')
		reply('private',source,u'английский – французский (ef)\n\
английский – немецкий (ed)\n\
английский – итальянский (ei)\n\
английский – корейский (ek)\n\
английский – японский (ej)\n\
английский – русский (er)\n\
русский – английский (re)\n\
английский – испанский (es)\n\
английский – португальский (ep)\n\
немецкий – французский (df)\n')
		return
	stsp=string.split(parameters, ' ', 1)
	if not len(stsp)>=2:
		reply(type,source,u'чего-то не хватает, прочти хелп')
	langpairs={'er': 'en ru', 're': 'ru en','ef': 'en fr','ed': 'en de', 'df': 'de fr','ei': 'en it', 'es': 'en sp', 'ep': 'en pt', 'ek': 'en ko', 'ej': 'en ja', 'ar': 'auto ru'}
	if langpairs.has_key(stsp[0]):
		pair=langpairs[stsp[0]]
		pair=string.split(pair, ' ', 1)
		answ = google_translate(pair[0],pair[1],stsp[1].encode('utf-8'))
		answ=answ.replace('&apos;', '\\').replace('&gt;', '>').replace('&lt;', '<').replace('<br>', '\n').replace('&quot;', '"').replace('&#39;', '\'')
		reply(type,source,unicode(answ))
	else:
		reply(type,source,u'что это за язык?')
		

register_command_handler(handler_google_trans, 'перевод', ['инфо','все'], 10, 'Переводит фразу на одном языке в другой. Подробнее - напишите "перевод языки".', 'перевод <исходный_язык> <нужный_язык> <фраза>', ['перевод er hello', 'перевод re привет'])
