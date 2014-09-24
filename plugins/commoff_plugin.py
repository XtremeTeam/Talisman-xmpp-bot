#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  commoff_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_commoff(type,source,parameters):
	na=[u'доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='dynamic/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if not y in commoff:
						commoff.append(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'						
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'For this conference the following commands have been disconnected:\n'+valcomm
		if alrcomm:
			rep+=u'\nthe Following commands have not been disconnected, as they are already disconnected:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nListed below a command at all commands :) :\n'+notvalcomm
		if npcomm:
			rep+=u'\nFollowing commands cannot be disconnected in general:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		for x in commoff:
			vcnt+=1
			valcomm+=str(vcnt)+u') '+x+u'\n'
		if valcomm:
			rep=u'In this conference following commands are disconnected:\n'+valcomm
		else:
			rep=u'In this conference all commands are included'
			
		
	reply(type,source,rep.strip())
		
def handler_common(type,source,parameters):
	na=[u'доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'свал',u'restart',u'globacc',u'команды',u'sh',u'exec',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='dynamic/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if y in commoff:
						commoff.remove(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'						
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'For this conference the following commands have been included:\n'+valcomm
		if alrcomm:
			rep+=u'\nFollowing commands have not been included, as they have not been disconnected:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nListed below a command at all commands :) :\n'+notvalcomm
		if npcomm:
			rep+=u'\nFollowing commands are not disconnected in general:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		rep=u'hmmmm?'
		
	reply(type,source,rep.strip())
	
def get_commoff(gch):
	try:
		if GCHCFGS[gch].has_key('commoff'):
			commoff=GCHCFGS[gch]['commoff']
			COMMOFF[gch]=commoff
		else:
			COMMOFF[gch]=gch
			COMMOFF[gch]=[]
	except:
		pass
	
	
register_command_handler(handler_commoff, 'commoff', ['admin','muc','all'], 20, 'Disconnects the certain commands for current conference, Without parameters shows the list of already disconnected commands.', 'commoff [Commands]', ['commoff','commoff тык диско версия пинг'])
register_command_handler(handler_common, 'common', ['admin','muc','all'], 20, 'to reactivate command in conference.', 'common [command]', ['common tyk disco version of ping'])

register_stage1_init(get_commoff)
