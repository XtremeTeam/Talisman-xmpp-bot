#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  macro_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def macroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		reply(type, source, u'мало аргументофф')
		return
	else:
		if pl[1].split()[0] in COMMAND_HANDLERS or pl[1].split()[0] in MACROS.gmacrolist or pl[1].split()[0] in MACROS.macrolist[source[1]]:
			real_access = MACROS.get_access(pl[1].split()[0], source[1])
			if real_access < 0 and pl[1].split()[0] in COMMAND_HANDLERS:
				real_access = COMMANDS[pl[1].split()[0]]['access']
			else:
				pass
			if real_access:
				if not has_access(source, real_access, source[1]):
					reply(type, source, u'размечтался ]:->')
					return
		else:
			reply(type, source, u'не вижу команду внутри макроса')
			return				
		MACROS.add(pl[0], pl[1], source[1])
		MACROS.flush()		
		reply(type, source, u'добавил')
	
def gmacroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'мало аргументофф'
	else:
		MACROS.add(pl[0], pl[1])
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'добавил'
	reply(type, source, rep)

def macrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters, source[1])
#		write_file('dynamic/'+source[1]+'macros.txt', str(MACROS.macrolist[source[1]]))
		MACROS.flush()
		rep = u'убил'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)
	
def gmacrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters)
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'убил'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source)
		if not rep:
			rep = u'не экспандится. прав маловато?'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)
	
def gmacroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source, '1')
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		try:
			if MACROS.macrolist[source[1]].has_key(parameters):
				rep = parameters+' -> '+MACROS.macrolist[source[1]][parameters]
		except:
			rep = u'нет такого макроса'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[source[1]][x] for x in MACROS.macrolist[source[1]]])
	if not rep:
		rep=u'мало прав'
	reply(type, source, rep)
	
def gmacroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		if MACROS.gmacrolist.has_key(parameters):
			rep = parameters+' -> '+MACROS.gmacrolist[parameters]
		else:
			rep = u'нет такого макроса'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[x] for x in MACROS.macrolist])
	reply(type, source, rep)
	
def macrolist_handler(type, source, parameters):
	rep,dsbll,dsblg,glist,llist=u'Cписок макросов:',[],[],[],[]
	if MACROS.macrolist[source[1]]:
		for macro in MACROS.macrolist[source[1]].keys():
			if macro in COMMOFF[source[1]]:
				dsbll.append(macro)
			else:
				llist.append(macro)
		dsbll.sort()
		llist.sort()
		rep += u'\nЛОКАЛЬНЫЕ\n'+', '.join(llist)
		if dsbll:
			rep+=u'\n\nСледующие локальные макросы отключены в этой конференции:\n'+', '.join(dsbll)
	else:
		rep+=u'\nнет локальных макросов'
	for macro in MACROS.gmacrolist.keys():
		if macro in COMMOFF[source[1]]:
			dsblg.append(macro)
		else:
			glist.append(macro)
	dsblg.sort()
	glist.sort()
	rep += u'\nГЛОБАЛЬНЫЕ\n'+', '.join(glist)
	if dsblg:
		rep+=u'\n\nСледующие глобальные макросы отключены в этой конференции:\n'+', '.join(dsblg)
	if type=='public':
		reply(type, source, u'ушёл')
	reply('private', source, rep)
	
def macroaccess_handler(type, source, parameters):
	if parameters:
		args,access = parameters.split(' '),10
		if len(args)==2:
			macro = args[0]
			if macro in COMMAND_HANDLERS:
				if not user_level(source,source[1])==100:
					reply(type,source,u'размечтался ]:->')
					return
				else:
					pass
			elif macro in MACROS.gmacrolist or macro in MACROS.macrolist[source[1]]:
				real_access = MACROS.get_access(macro, source[1])
				if real_access < 0:
					pass
				else:
					if not has_access(source, real_access, source[1]):
						reply(type,source,u'размечтался ]:->')
						return
			try:
				access = int(args[1])
			except:
				reply(type,source,u'синтакс инвалид')
				return
			MACROS.give_access(macro,access,source[1])
			reply(type,source,u'дал')
			time.sleep(1)
			MACROS.flush()
		else:
			reply(type,source,u'что за бред?')
			
def gmacroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access)
			reply(type,source,u'дал')
			time.sleep(1)
			write_file('dynamic/macroaccess.txt', str(MACROS.gaccesslist))
		else:
			reply(type,source,u'что за бред?')


register_command_handler(macroadd_handler, 'macroadd', ['админ','макро','все'], 20, 'Добавить макро. Само макро должно быть заключено в апострофы `` !!!', 'macroadd [название] [`макро`]', ['macroadd глюк `сказать /me подумал, что все глючат`'])
register_command_handler(gmacroadd_handler, 'gmacroadd', ['суперадмин','макро','все'], 100, 'Добавить макро глобально. Само макро должно быть заключено в апострофы `` !!!', 'gmacroadd [название] [`макро`]', ['gmacroadd глюк `сказать /me подумал, что все глючат`'])

register_command_handler(macrodel_handler, 'macrodel', ['админ','макро','все'], 20, 'Удалить макро.', 'macrodel [название]', ['macrodel глюк'])
register_command_handler(gmacrodel_handler, 'gmacrodel', ['суперадмин','макро','все'], 100, 'Удалить глобальное макро.', 'macrodel [название]', ['macrodel глюк'])

register_command_handler(macroexpand_handler, 'macroexp', ['админ','макро','инфо','все'], 20, 'Развернуть макро, т.е. посмотреть на готовое макро в сыром виде.', 'macroexp [название] [параметры]', ['macroexp админ бот'])
register_command_handler(gmacroexpand_handler, 'gmacroexp', ['суперадмин','макро','инфо','все'], 100, 'Развернуть макро, т.е. посмотреть на него в сыром виде.', 'gmacroexp [название] [параметры]', ['gmacroexp админ бот'])

register_command_handler(macroinfo_handler, 'macroinfo', ['админ','макро','инфо','все'], 20, 'Открыть макро, т.е. просто посмотреть как выглядит макро. Чтобы посмотреть на все макро напишите вместо названия определённого макро "allmac" без кавычек.', 'macroinfo [название]', ['macroinfo глюк','macroinfo allmac'])
register_command_handler(gmacroinfo_handler, 'gmacroinfo', ['суперадмин','макро','инфо','все'], 100, 'Открыть макро (любое), т.е. просто посмотреть как выглядит макро. Чтобы посмотреть на все макро напишите вместо названия определённого макро "allmac" без кавычек.', 'macroinfo [название]', ['macroinfo глюк','macroinfo allmac'])

register_command_handler(macrolist_handler, 'macrolist', ['хелп','макро','инфо','все'], 10, 'Список макро.', 'macrolist', ['macrolist'])

register_command_handler(macroaccess_handler, 'macroaccess', ['админ','макро','все'], 20, 'Изменить доступ к определённому макро.', 'macroaccess [макро] [доступ]', ['macroaccess глюк 10'])
register_command_handler(gmacroaccess_handler, 'gmacroaccess', ['суперадмин','макро','все'], 100, 'Изменить доступ к определённому макро (любому).', 'gmacroaccess [макро] [доступ]', ['macroaccess админ 20'])
