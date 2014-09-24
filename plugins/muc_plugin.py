#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  muc_plugin.py

#  Initial Copyright © 2009 dr.Schmurge <JID: dr.schmurge@gajim.org>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details. 


aff_pending=[]
def handler_aff(typ, source, parameters):
	aff_list={u"moder":{'role':'moderator'},u"member": {'affiliation':'member'},u"participant":{'role':'participant'},u"outcast": {'affiliation':'outcast'},u'owner':{'affiliation':'owner'},u'admin':{'affiliation':'admin'}}
	#if typ=="public":
		#reply(typ, source, u"Дурик, это надо писать в приват!")
		#return

	if not aff_list.has_key(parameters):
		reply(typ, source, u"i dont know that word!")
		return

	groupchat=source[1]
	id = 'a'+str(random.randrange(1, 1000))
	globals()['aff_pending'].append(id)
	iq=xmpp.Iq('get',to=groupchat,queryNS=xmpp.NS_MUC_ADMIN,xmlns=None)
	iq.getQueryChildren().append(xmpp.Protocol('item',attrs=aff_list[parameters]))
	iq.setID(id)
	param=''
	JCON.SendAndCallForResponse(iq, handler_aff_answ,{'mtype': typ, 'source': source, 'param': param})
	return

def handler_aff_answ(coze, res, mtype, source, param):
	id = res.getID()
	if id in globals()['aff_pending']:
		globals()['aff_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
		#-=
			aa=res.getTag("query")
                        if aa==None:
                                rep=u"fatal error, unable to query"
                        else:
                                m=aa.getTags("item")
                                if len(m)==0:
                                        rep=u"empty"
                                else:
                                        rep=""
                                        for t in m:
                                                ats=t.getAttrs()
                                                if ats.has_key("jid"):
                                                        rep+=t["jid"]+" "
                                                if ats.has_key("affiliation"):
                                                        rep+=t["affiliation"]+" "
                                                if ats.has_key("role"):
                                                        rep+=t["role"]+" "
                                                reas=t.getTag("reason")
                                                if reas!= None:
                                                        dt=reas.getData()
                                                        if dt!=None:
                                                                rep+=dt+" "
                                                rep+="\n"
		#-=
		else:
			rep = u'i can not!!!'
	if mtype=="public":
		reply(mtype, source, u"sent to private")
	reply("private", source, rep)
	

def handler_bot_nick(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		add_gch(source[1], parameters)
		join_groupchat(source[1], parameters)
	reply(type, source, u'OK')

def handler_admin(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				jid = get_true_jid(groupchat+'/'+nick)
				order_admin(groupchat, jid, u'')
				return

def handler_owner(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				jid = get_true_jid(groupchat+'/'+nick)
				order_owner(groupchat, jid, u'')
				return

def handler_unban(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		jid = parameters
		order_unban(groupchat, jid)
		reply(type, source, u'it is done :)')
		return

def handler_admin(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				jid = get_true_jid(groupchat+'/'+nick)
				order_admin(groupchat, jid, u'')
				return
				
def handler_ban(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		if not parameters.count('@'):
			nick = parameters
			if GROUPCHATS.has_key(source[1]):
				if not nick in GROUPCHATS[groupchat]:
					reply(type, source, u'who?')
					return
				else:
					jid = get_true_jid(groupchat+'/'+nick)
					order_banjid(groupchat, jid, u'')
					reply(type, source, u'it is done')
					return
		else:
			jid = parameters
			order_banjid(groupchat, jid, u'')
			reply(type, source, u'it is done')
			return

def handler_ban_nick(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				jid = get_true_jid(groupchat+'/'+nick)
				order_banjid(groupchat, jid, u'')
				reply(type, source, u':)')
				return
		
def handler_ban_jid(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	else:
	        if not parameters.count(' '):
			jid = parameters
			order_banjid(groupchat, jid, u'')
			reply(type, source, u':)')
			return
		else:
			parameters = parameters.split()
			jid = parameters[0]
			order_banjid(groupchat, jid, parameters[1])
			reply(type, source, u':)')
			return
			
def handler_visitor(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'what?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				#jid = get_true_jid(groupchat+'/'+nick)
				order_visitor(groupchat, nick, u'')
				reply(type, source, u':)')
				return

def handler_participant(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'what?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				#jid = get_true_jid(groupchat+'/'+nick)
				order_participant(groupchat, nick, u'')
				reply(type, source, u':)')
				return

def handler_kick(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'what?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				#jid = get_true_jid(groupchat+'/'+nick)
				order_kick(groupchat, nick, u'')
				reply(type, source, u':)')
				return

def handler_member(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'what?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				jid = get_true_jid(groupchat+'/'+nick)
				order_member(groupchat, jid, u'')
				reply(type, source, u':)')
				return

def handler_moderator(type, source, parameters):
	groupchat = source[1]
	if not parameters:
		reply(type, source, u'what?')
		return
	else:
		nick = parameters
		if GROUPCHATS.has_key(source[1]):
			if not nick in GROUPCHATS[groupchat]:
				reply(type, source, u'who?')
				return
			else:
				#jid = get_true_jid(groupchat+'/'+nick)
				order_moderator(groupchat, nick, u'')
				reply(type, source, u':)')
				return

#def handler_unmember(type, source, parameters):
	#groupchat = source[1]
	#if not parameters:
		#reply(type, source, u'Кого?')
		#return
	#else:
		#nick = parameters
		#if GROUPCHATS.has_key(source[1]):
			#if not nick in GROUPCHATS[groupchat]:
				#reply(type, source, u'А он тут?')
				#return
			#else:
				#jid = get_true_jid(groupchat+'/'+nick)
				#order_unmember(groupchat, jid)
				#reply(type, source, u'Готово')
				#return

def handler_where(type, source, parameters):
	#reply(type, source, 'я сижу в '+str(len(GROUPCHATS.keys()))+' комнатах:\n'+'\n'.join(GROUPCHATS.keys()).encode('utf8')) #+' ['+str(len(GROUPCHATS.has_key(GROUPCHATS.keys()))))
	cnt = 0
	gch = ''
	gch_cnt = []
	for gch in GROUPCHATS.keys():
		for nicks in GROUPCHATS[gch]:
			#if user_level(gch+'/'+nicks,gch)>=0:
				cnt += 1
		gch_cnt.append((gch, cnt))
		cnt = 0
	n = 1
	msg = u'Total number of conferences: '+str(len(gch_cnt))+'\n'
	for i in gch_cnt:
		msg += str(n)+'. '+i[0]+' ['+str(i[1])+']\n'
		n += 1
	reply(type, source, msg)
	
#def handler_who_was(type, source, parameters):
	#gch = source[1]
	#for x in GROUPCHATS[gch].keys():
		#x = x.encode("utf-8")
	#reply(type, source, u'я здесь видела '+str(len(GROUPCHATS[gch].keys()))+' юзеров:\n'+', '.join([x]))

def handler_ban_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_banjid(gch, jid, u'fuck off')
	     
def handler_kick_everywhere(type, source, nick):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_kick(gch, nick, u'fuck off')

def handler_unban_everywhere(type, source, jid):
	gch=source[1]
	for gch in GROUPCHATS.keys():
	    order_unban(gch, jid)
	  
def order_admin(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'admin'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_owner(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'owner'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

def order_participant(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'participant'})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_ban(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_banjid(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_member(groupchat, jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'member'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_moderator(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'moderator'})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_unmember(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID(str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':"none"})
	iq.addChild(node=query)
	JCON.send(iq)

register_command_handler(handler_aff, 'aff', ['info','muc','admin','all'], 20, 'show affiliation list in the current conference', 'aff <type>', ['aff owner','aff admin','aff moderator','aff member','aff participant','aff outcast'])
register_command_handler(handler_bot_nick, 'botnick', ['muc','all'], 20, 'changes the bots nickname in conference.', 'botnick <nick>', ['botnick pink'])
register_command_handler(handler_admin, 'admin', ['muc','all'], 30, 'to let bot make someone an admin of conference.', 'admin <nick>', ['admin joe'])
register_command_handler(handler_owner, 'owner', ['muc','all'], 30, 'bot will make the specified person an ownerof the conference.', 'owner <nick>', ['owner fred'])
register_command_handler(handler_unban, 'unban', ['muc','all'], 20, 'to unban a person from the conference.', 'unban <jid>', ['unban planb@talkonaut.com'])
register_command_handler(handler_ban, 'ban', ['muc','all'], 20, 'ban someone from conference you can also specify a reason for the ban', 'ban <nick/jid> <reason>', ['ban joe@server.dom', 'ban joe', 'ban joe asshole'])
register_command_handler(handler_ban_nick, 'bannick', ['muc','all'], 20, 'ban nick from room you can also give a reason for the ban', 'ban <nick>', ['ban sammy', 'ban sammy flood'])
register_command_handler(handler_ban_jid, 'banjid', ['muc','all'], 20, 'ban of JID, bot will save the specified jid in the ban list thus preventing him or her from entering the conference', 'banjid <JID>', ['banjid user@server.dom'])
register_command_handler(handler_visitor, 'visitor', ['muc','all'], 20, 'to make someone a visitor in conference note that he or she might not be able to send messages directly in the conference', 'visitor <nick>', ['visitor sammy'])
register_command_handler(handler_participant, 'participant', ['muc','all'], 20, 'makes the given nick a participant and granting him voice', 'participant <nick>', ['participant leon'])
register_command_handler(handler_kick, 'kick', ['muc','all'], 15, 'kicks person out of the conference, you can also give a reason for the kick', 'kick <nick> <reason>', ['kick sam', 'kick sam spamming'])
register_command_handler(handler_member, 'member', ['muc','all'], 20, 'gives the role of member to a participant in conference', 'member <nick>', ['member roxy'])
register_command_handler(handler_moderator, 'mod', ['muc','all'], 20, 'gives soneone the role of moderator note moderators can see jid of others and can also kick', 'mod <nick>', ['mod genko'])
#register_command_handler(handler_member, 'унмембер', ['мук','все'], 20, 'Забрать права зарегистрированного участника чата', 'унмембер <nick>', ['унмембер Вася'])
register_command_handler(handler_where, 'show', ['muc','all'], 100, 'shows the list where bot is currently active', 'show', ['show'])
register_command_handler(handler_kick_everywhere, 'fullkick', ['superadmin','all'], 100, 'to kick a nick everywhere where bot sits in conference', 'fullkick nick', ['fullkick joe'])
register_command_handler(handler_ban_everywhere, 'fullban', ['superadmin','all'], 100, 'to ban a jid everywhere where bot sits in conference', 'fullban jid', ['fullban vasya_pupkin@jabber.ru'])
register_command_handler(handler_unban_everywhere, 'fullunban', ['superadmin','all'], 100, 'to unban a jid everywhere bot sits', 'fullunban jid', ['fullunban vasya_pupkin@jabber.ru'])
#register_command_handler(handler_who_was, 'хтобыл', ['мук','все'], 20, 'Показывает ники всех, кто заходил в комнату за текущую сессию бота', 'хтобыл', ['хтобыл'])
