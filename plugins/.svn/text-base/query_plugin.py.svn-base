#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  query_plugin.py

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

def handler_query_get_public(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	if parameters:
		if localdb.has_key(string.lower(parameters)):
			reply(type, source, u'про <' + parameters + u'> я знаю следующее:\n' + localdb[string.lower(parameters)])
		else:
			reply(type, source, u'я хз что такое <' + parameters + '> :(')
	else:
			reply(type, source, u'ииии?')

def handler_query_get_private(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
		return
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	tojid = ''
	rep = u'кому?'
	localdb = eval(read_file(DBPATH))
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if get_bot_nick(groupchat) != nick:
				if nick in nicks:
					tojid = groupchat+'/'+nick
		else:
			tojid = groupchat+'/'+source[2]
			body = parameters
	if tojid:
		if localdb.has_key(string.lower(body)):
			if type == 'public':
				reply(type, source, u'ушло')
			msg(tojid, u'про <' + body + u'> я знаю следующее:\n\n'+localdb[string.lower(body)])
		else:
			reply(type, source, u'я хз что такое <' + body + '> :(')
	else:
		reply(type, source, u'кому?')

		
def handler_query_get_random(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	if not localdb.keys():
		reply(type, source, u'база пуста!')
		return
	rep = random.choice(localdb.keys())
	reply(type, source, u'про <' + rep + u'> я знаю следуюущее:\n' + localdb[rep])


def handler_query_set(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
		return
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		keyval = string.split(parameters, '=', 1)
		if not len(keyval)<2:
			key = string.lower(keyval[0]).strip()
			value = keyval[1].strip()
			if not value:
				if localdb.has_key(key):
					del localdb[key]
				reply(type, source, key + u' -> прибил нафиг')
			else:
				localdb[key] = keyval[1].strip()+u' (from '+source[2]+')'
				reply(type, source, u'теперь я буду знать, что такое ' + key)
			write_file(DBPATH, str(localdb))
		else:
			reply(type, source, u'ииии?')
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')

def handler_query_count(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=str(len(localdb.keys()))
		reply(type, source, 'в базе ответов/вопросов данной конфы '+num+' записей')
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return

def handler_query_search(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
		return
	rep=[]
	groupchat=source[1]	
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		if not localdb.keys():
			reply(type, source, u'база пуста!')
			return
		for x in localdb:
			if x.count(parameters)>0:
				rep.append(x)
		if rep:
			reply(type,source,u'совпало с:\n'+', '.join(rep))
		else:
			reply(type,source,u'ни с чем не совпало :(')
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
		
def handler_query_all(type, source, parameters):
	groupchat=source[1]
	DBPATH='dynamic/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=len(localdb.keys())
		if num == 0:
			reply(type, source, 'база пуста!')
			return
		reply(type, source, ', '.join(localdb.keys()))
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return


register_command_handler(handler_query_get_public, '???', ['инфо','wtf','все'], 10, 'Ищет ответ на вопрос в локальной базе (аналог wtf в сульцах).', '??? <запрос>', ['??? что-то', '??? что-то ещё'])
register_command_handler(handler_query_get_private, '!??', ['инфо','wtf','все'], 10, 'Ищет ответ на вопрос в локальной базе и посылает его в приват (аналог !word showpriv в глюксах).', '!?? <ник> <запрос>', ['!?? что-то', '!?? guy что-то'])
register_command_handler(handler_query_set, '!!!', ['инфо','wtf','админ','все'], 11, 'Устанавливает ответ на вопрос в локальной базе (аналог dfn в сульцах).', '!!! <запрос> = <ответ>', ['!!! что-то = the best!', '!!! что-то ещё ='])
register_command_handler(handler_query_count, '???count', ['инфо','wtf','все'], 10, 'Показывает количество вопросов в базе конфы (аналог wtfcount в сульцах).', '!!! ???count', ['???count'])
register_command_handler(handler_query_get_random, '???rand', ['инфо','wtf','все'], 10, 'Показывает случайно выбранный ответ на вопрос (аналог wtfrand в сульцах).', '???rand', ['???rand'])
register_command_handler(handler_query_search, '???search', ['инфо','wtf','все'], 10, 'Поиск по базе.', '???search <запрос>', ['???search что-то'])
register_command_handler(handler_query_all, '???all', ['инфо','wtf','все'], 10, 'Показывает все ключи базы (осторожно, может быть много!).', '???all', ['???all'])
