#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  google_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

google_last_res = []
import google

def google_remove_html(text):
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

def google_search(query, cont=False):
	global google_last_res
	if cont:
		if not google_last_res:
			return 'нет ничего для тебя :('
	else:
		if query:
			data = google.doGoogleSearch(query)
		else:
			return u'а чё искать-то?'
	try:
		if not cont:
			first = data.results[0]
			google_last_res = data.results[1:]
		else:
			first = google_last_res[0]
			google_last_res = google_last_res[1:]
		url = first.URL
		title = google_remove_html(first.title)
		if first.summary:
			summary = google_remove_html(first.summary)
		else:
			summary = google_remove_html(first.snippet)
		if cont:
			return url + '\n' + title + '\n' + summary
		else:
			total = str(data.meta.estimatedTotalResultsCount)
			return url + '\n' + title + '\n' + summary
	except:
		return 0

def handler_google_google(type, source, parameters):
	results = google_search(parameters, parameters == u'еще')
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'ничё не нашёл :(')

def handler_google_xepsearch(type, source, parameters):
	results = google_search('allinurl: XEP-'+ parameters + ' site:http://www.xmpp.org/extensions')
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'ничё не нашёл :(')

register_command_handler(handler_google_google, 'гугль', ['инфо','все'], 10, 'Искать что-то в инете.', 'гугль <запрос>', ['search что-то'])
register_command_handler(handler_google_xepsearch, 'xep', ['инфо','все'], 10, 'Ищет описание заданного XEP\'а.', 'xep (англ. буквы) <номер>', ['xep 0045'])
