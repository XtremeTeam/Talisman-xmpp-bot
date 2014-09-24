#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  weather_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploru.net>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import pymetar

WEATHERCODE_FILE = 'static/weather.txt'

def handler_weather_weather(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
		return
	try:
		rf=pymetar.ReportFetcher(parameters.strip())
		fr=rf.FetchReport()
	except Exception, ex:
		results = u'а если ли такой код?'
		return
	rp=pymetar.ReportParser()
	pr=rp.ParseReport(fr)
	tm=time.strptime(pr.getISOTime(), '%Y-%m-%d %H:%M:%SZ')
	tm=time.strftime('%H:%M:%S',tm)
	rep = u'погода в %s (%s) на %s\n%s, temperature: %s° C, humidity: %s%%, ' %(pr.getStationName(), parameters.strip(), tm, pr.getWeather(), pr.getTemperatureCelsius(), pr.getHumidity())
	if pr.getWindSpeed():
		rep+='wind: %s, ' %(pr.getWindSpeed())
	if pr.getPressure():
		rep+='pressure: %s, ' %(pr.getPressure())
	rep+='sky conditions: %s' %(pr.getSkyConditions())
	reply(type, source, rep)

def handler_weather_weathercode(type, source, parameters):
	if not parameters:
		reply(type, source, u'чё-то ты не то написал...')
		return
	if len(parameters)<=2:
		reply(type, source, u'какая-то фигня...')
		return
	results = ''
	query = string.lower(parameters)
	fp = open(WEATHERCODE_FILE, 'r')
	lines = fp.readlines()
	for line in lines:
		if string.count(string.lower(line), query):
			results += string.split(line, '=> ')[0]
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'хз')

register_command_handler(handler_weather_weather, 'погода', ['инфо','все'], 10, 'Смотрит погоду из NOAA', 'погода <4буквенный_код_города>', ['погода ukhh'])
register_command_handler(handler_weather_weathercode, 'код', ['инфо','все'], 10, 'Показывает код города для просмотра погоды', 'код <город>', ['код orel'])
