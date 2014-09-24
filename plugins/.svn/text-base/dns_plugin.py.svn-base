#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  dns_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import socket

def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(query)
			return u', '.join(ipaddrlist)
		except socket.gaierror:
			return u'не нахожу что-то :('
	else:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		except socket.herror:
			return u'не нахожу что-то :('
		return hostname + ' ' + string.join(aliaslist) + ' ' + string.join(aliaslist)

def handler_dns_dns(type, source, parameters):
	if parameters.strip():
		result = dns_query(parameters)
		reply(type, source, result)
	else:
		reply(type, source, u'что это было?')

register_command_handler(handler_dns_dns, 'днс', ['инфо','все'], 10, 'Показывает ответ от DNS для определённого хоста или IP адреса.', 'днс <хост/IP>', ['днс jabber.aq', 'днс 127.0.0.1'])
