#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  admin_plugin.py

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

def popups_check(gch):
	DBPATH='dynamic/'+gch+'/config.cfg'
	if GCHCFGS[gch].has_key('popups'):
		if GCHCFGS[gch]['popups'] == 1:
			return 1
		else:
			return 0
	else:
		GCHCFGS[gch]['popups']=1
		write_file(DBPATH,str(GCHCFGS[gch]))
		return 1
				
def handler_admin_join(type, source, parameters):
	if parameters:
		passw=''
		args = parameters.split()
		if len(args)>1:
			groupchat = args[0]
			passw = string.split(args[1], 'pass=', 1)
			if not passw[0]:
				reason = ' '.join(args[2:])
			else:
				reason = ' '.join(args[1:])
		else:
			groupchat = parameters
			reason = ''
		get_gch_cfg(groupchat)
		for process in STAGE1_INIT:
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,process,'atjoin_init'+str(INFO['thr']),(groupchat,)).start()
		DBPATH='dynamic/'+groupchat+'/config.cfg'
		write_file(DBPATH, str(GCHCFGS[groupchat]))
		if passw:
			add_gch(groupchat, DEFAULT_NICK)
			join_groupchat(groupchat, DEFAULT_NICK)
		else:
			add_gch(groupchat, DEFAULT_NICK, passw)
			join_groupchat(groupchat, DEFAULT_NICK, passw)
		MACROS.load(groupchat)
		reply(type, source, u'joined -> <' + groupchat + '>')
		if popups_check(groupchat):
			if reason:
				msg(groupchat, u'sent by '+source[2]+u' reason:\n'+reason)
			else:
				msg(groupchat, u'sent by '+source[2])
	else:
		reply(type, source, u'need to write conference and the reason (not needed for reason)')

def handler_admin_leave(type, source, parameters):
	args = parameters.split()
	if len(args)>1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'i am not there at present')
			return
		reason = ' '.join(args[1:]).strip()
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'i am not there!')
			return
		groupchat = args[0]
	elif len(args)==1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'try, again')
			return
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'And I there was not present')
			return
		reason = ''
		groupchat = args[0]
	else:
		groupchat = source[1]
		reason = ''
	if popups_check(groupchat):
		if reason:
			msg(groupchat, u'removed '+source[2]+u' reason:\n'+reason)
		else:
			msg(groupchat, u'removed '+source[2])
	if reason:
		leave_groupchat(groupchat, u'left '+source[2]+u' reason:\n'+reason)
	else:
		leave_groupchat(groupchat,u'left from '+source[2])
	reply(type, source, u'I have left from -> <' + groupchat + '>')


def handler_admin_msg(type, source, parameters):
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'message sent')
	
def handler_glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'news from '+source[2]+u':\n'+parameters+u'\nI remind that as usual all a help can be got writing a "help".\nAbout all of glitches, errors, and also ask suggestions and structural criticism to send me thus: we write to "pass '+source[2]+u' and here your report", naturally without quotation marks.\nTHANK YOU FOR ATTENTION!')
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'message sent in '+str(totalblock)+' conferences (from '+str(total)+')')
		
def handler_glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'news from '+source[2]+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'message sent in '+str(totalblock)+' conferences (from '+str(total)+')')
	

def handler_admin_say(type, source, parameters):
	if parameters:
		args=parameters.split()[0]
		msg(source[1], parameters)
	else:
		reply(type, source, u'did not forget to write a message?')

def handler_admin_restart(type, source, parameters):
	if parameters:
		reason = parameters
	else:
		reason = ''
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'im restarting '+source[2]+u' reason:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'restart '+source[2])
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': restart -> '+reason)
	else:
		prs.setStatus(source[2]+u': restart')
	JCON.send(prs)
	time.sleep(1)
	JCON.disconnect()

def handler_admin_exit(type, source, parameters):
	if parameters:
		reason = parameters
	else:
		reason = ''
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'i was turned off '+source[2]+u' for reason:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'i was turned off '+source[2])
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': i am switched off -> '+reason)
	else:
		prs.setStatus(source[2]+u': i am switched off')
	JCON.send(prs)
	time.sleep(2)
	os.abort()
	
def handler_popups_onoff(type, source, parameters):
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'syntax disabled')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['popups']=1
			reply(type,source,u'global notifications are turned on')
		else:
			GCHCFGS[source[1]]['popups']=0
			reply(type,source,u'global notifications are turned off')
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['popups']
		if ison==1:
			reply(type,source,u'here global notifications are turned on')
		else:
			reply(type,source,u'here global notifications are turned off')
			
def handler_botautoaway_onoff(type, source, parameters):
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'syntax disabled')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['autoaway']=1
			reply(type,source,u'autoaway mode on')
		else:
			GCHCFGS[source[1]]['autoaway']=0
			reply(type,source,u'autoaway mode off')
		get_autoaway_state(source[1])
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['autoaway']
		if ison==1:
			reply(type,source,u'here included')
		else:
			reply(type,source,u'Here autoabsence is disconnected')	
	
def handler_changebotstatus(type, source, parameters):
	if parameters:
		args,show,status=parameters.split(' ',1),'',''
		if args[0] in ['away','xa','dnd','chat']:
			show=args[0]
		else:
			show=None
			status=parameters
		if not status:
			try:
				status=args[1]
			except:
				status=None
		change_bot_status(source[1],status,show,0)
		GCHCFGS[gch]['status']={'status': status, 'show': show}
	else:
		stmsg=GROUPCHATS[source[1]][get_bot_nick(source[1])]['stmsg']
		status=GROUPCHATS[source[1]][get_bot_nick(source[1])]['status']
		if stmsg:
			reply(type,source, u'I am now '+status+u' ('+stmsg+u')')
		else:
			reply(type,source, u'i am now '+status)
			
def get_autoaway_state(gch):
	if not 'autoaway' in GCHCFGS[gch]:
		GCHCFGS[gch]['autoaway']=1
	if GCHCFGS[gch]['autoaway']:
		LAST['gch'][gch]['autoaway']=0
		LAST['gch'][gch]['thr']=None
		
def set_default_gch_status(gch):
	if isinstance(GCHCFGS[gch].get('status'), str): #temp workaround
		GCHCFGS[gch]['status']={'status': u'write "commands all" for the list of commands and "macrolist" for the list of macros', 'show': u''}
	elif not isinstance(GCHCFGS[gch].get('status'), dict):
		GCHCFGS[gch]['status']={'status': u'write "commands all" for the list of commands and "macrolist" for the list of macros', 'show': u''}


register_command_handler(handler_admin_join, 'join', ['superadmin','muc','all'], 40, 'Join conf. If there is a password write that password right after the name of conference.', 'join <conf> [pass=1111] [reason]', ['join stream@conference.jabbus.org', 'join stream@conference.jabbus.org *VICTORY*', 'join stream@conference.jabbus.org pass=1111 *VICTORY*'])
register_command_handler(handler_admin_leave, 'leave', ['admin','muc','all'], 100, 'Forces to leave from current or certain conference.', 'leave <conference> [reason]', ['leave joe@conference.jabber.aq hate you', 'leave sleep','свал'])
register_command_handler(handler_admin_msg, 'msg', ['admin','muc','all'], 40, 'Sends message on behalf of bot certain JID.', 'message <jid> <message>', ['message guy@jabbus.org *HI* Chuvak!'])
register_command_handler(handler_admin_say, 'say', ['admin','muc','all'], 20, 'say <message>', ['say *HI* peoples'])
register_command_handler(handler_admin_restart, 'restart', ['superadmin','all'], 100, 'Restart bot.', 'restart [reason]', ['restart','restart *FIGA*'])
register_command_handler(handler_admin_exit, 'exit', ['superadmin','all'], 100, 'Complete out.', 'exit [reason]', ['exit','say <message>'])
register_command_handler(handler_glob_msg, 'globmsg', ['superadmin','muc','all'], 100, 'Send message to all conf, which a bot is in.', 'globmsg [message]', ['globmsg all *HI*'])
register_command_handler(handler_glob_msg_help, 'hglobmsg', ['superadmin','muc','all'], 100, 'Send message to all conf, which a bot is in.', 'globmsg [message]', ['globmsg all *HI*'])
register_command_handler(handler_popups_onoff, 'popups', ['admin','muc','all'], 30, 'Off (0) On (1) message about join/leaves, restarts/off, and also global news for certain conf. Without a parameters will rotin current status.', 'popups [conf] [1|0]', ['popups stream@conference.jabbus.org 1','popups stream@conference.jabbus.org 0','popups'])
register_command_handler(handler_botautoaway_onoff, 'autoaway', ['admin','muc','all'], 30, 'Disconnects (0) Or includes (1) Autochange of the status of the bot to away  absence of commands of 10 minutes. Without parameter will show a current condition.', 'autoaway [1|0]', ['autoaway 1','autoaway'])
register_command_handler(handler_changebotstatus, 'setstatus', ['admin','muc','all'], 21, 'changes the status of the bot in conference list:\naway - no,\nxa - For a long time I am absent,\ndnd - do not disturb,\nchat - want to chat,\nа Also the status message (If it is given).', 'setstatus [status] [message]', ['setstatus away','setstatus away i am busy'])

register_stage1_init(get_autoaway_state)
register_stage1_init(set_default_gch_status)
