#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  help_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_help_help(type, source, parameters):
	ctglist = []
	if parameters and COMMANDS.has_key(parameters.strip()):
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nКатегории: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nИспользование: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nПримеры:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nНеобходимый уровень доступа: ' + str(COMMANDS[parameters.strip()]['access'])
		if parameters.strip() in COMMOFF[source[1]]:
			rep += u'\nЭта команда отключена в этой конференции!!!'
		else:
			pass
	else:
		rep = u'напиши слово "команды" (без кавычек), чтобы получить список команд, "помощь <команда>" для получения помощи по команде, macrolist для получения списка макросов, а также macroacc <макрос> для получения уровня доступа к определёному макросу\np.s. уровень доступа смотрите в привате'
	reply(type, source, rep)

def handler_help_commands(type, source, parameters):
	date=time.strftime('%d %b %Y (%a)', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep,dsbl = [],[]
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[x]['category']) and x) or None for x in COMMANDS]) - set([None])
		if not catcom:
			reply(type,source,u'а есть и такая? :-O')
			return
		for cat in catcom:
			if has_access(source, COMMANDS[cat]['access'],groupchat):
				if cat in COMMOFF[source[1]]:
					dsbl.append(cat)
				else:
					rep.append(cat)
					total = total + 1
		if rep:
			if type == 'public':
				reply(type,source,u'ушли')
			rep.sort()
			answ=u'Список команд в категории <'+parameters+u'> на '+date+u':\n\n' + u', '.join(rep) +u' - ('+str(total)+u' штук)'
			if dsbl:
				dsbl.sort()
				answ+=u'\n\nСледующие команды отключены в этой конференции:\n\n'+', '.join(dsbl)
			reply('private', source,answ)
		else:
			reply(type,source,u'размечтался ]:->')
	else:
		cats = set()
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type,source,u'ушли')
		reply('private', source, u'Список категорий на '+date+u'\n'+ cats+u'\n\nДля просмотра списка команд содержащихся в категории наберите "команды категория" без кавычек, например "команды все"')


register_command_handler(handler_help_help, 'помощь', ['хелп','инфо','все'], 0, 'Даёт основную справку или посылает информацию об определённой команде.', 'помощь [команда]', ['помощь', 'помощь пинг'])
register_command_handler(handler_help_commands, 'команды', ['хелп','инфо','все'], 0, 'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', 'команды [категория]', ['команды','команды все'])
