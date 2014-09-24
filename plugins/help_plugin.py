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
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nCategories: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nUse: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nExamples:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nIndispensable level of access: ' + str(COMMANDS[parameters.strip()]['access'])
		if parameters.strip() in COMMOFF[source[1]]:
			rep += u'\nThis command is disconnected in this conference!!!'
		else:
			pass
	else:
		rep = u'write "commands" (without quotation marks), to get the list of commands, "help <command>" for the help on a command, "macrolist" for list of macros, and also macroacc <macro> for the receipt of level of access to the certain macro\np.s. look the level of access in private'
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
			reply(type,source,u'does not exist? :-O')
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
				reply(type,source,u'private')
			rep.sort()
			answ=u'The list of commands in the category <'+parameters+u'> On '+date+u':\n\n' + u', '.join(rep) +u' - ('+str(total)+u' Pieces)'
			if dsbl:
				dsbl.sort()
				answ+=u'\n\nFollowing commands are disconnected in this conference:\n\n'+', '.join(dsbl)
			reply('private', source,answ)
		else:
			reply(type,source,u'Was lost in day-dreams ]:->')
	else:
		cats = set()
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type,source,u'private')
		reply('private', source, u'The list of categories on '+date+u'\n'+ cats+u'\n\nFor viewing the list of commands occuring a category type " commands <category> " without inverted commas, for example "commands all"')


register_command_handler(handler_help_help, 'help', ['help','info','all'], 0, 'Gives a basic certificate or sends information about a certain command.', 'help [command]', ['help', 'help ping'])
register_command_handler(handler_help_commands, 'commands', ['help','info','all'], 0, 'Shows the list of all of categories of commands. At the query of category shows the list of commands being in it.', 'commands [category]', ['commands','commands all'])
