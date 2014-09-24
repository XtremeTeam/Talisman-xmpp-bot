#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  fact_plugin.py

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

ELEMENT_FILE = 'static/elements.txt'
TLD_FILE = 'static/tlds.txt'
TLD_FILE = 'static/tlds.txt'

def fact_element(query):
	fp = open(ELEMENT_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		(key, value) = string.split(line, ' ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def fact_tld(query):
	fp = open(TLD_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		(key, value) = string.split(line, ': ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def handler_fact_element(type, source, parameters):
	result = fact_element(parameters.strip())
	smsg(type, source, result)

def handler_fact_tld(type, source, parameters):
	result = fact_tld(parameters.strip())
	smsg(type, source, result)

def fact_tld(query):
	fp = open(TLD_FILE, u'r')
	while 1:
		line = fp.readline()
		if not line:
			return u'Has not found :('
		(key, value) = string.split(line, ': ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def handler_fact_tld(type, source, parameters):
	result = fact_tld(parameters.strip())
	reply(type, source, result)


register_command_handler(handler_fact_element, 'element', ['fun','superadmin','muc','all'], 0, 'Returns the name and number of an atomic element code.', 'element <code>', ['element Li'])

register_command_handler(handler_fact_tld, '!tld', ['fun','superadmin','muc','all'], 0, 'Returns the location for a top level domain or a TLD for a location.', '!tld <location/TLD>', ['tld com', 'tld antarctica'])

register_command_handler(handler_fact_tld, 'tld', ['info','all'], 10, 'Показвает a finding of the domain of the first level (Geographical).', 'tld <The name/Reduction>', ['tld ru', 'tld russia'])
