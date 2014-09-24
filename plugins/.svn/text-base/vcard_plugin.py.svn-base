#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  vcard_plugin.py

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

vcard_pending=[]

def handler_vcardget(type, source, parameters):
	vcard_iq = xmpp.Iq('get')
	id='vcard'+str(random.randrange(1000, 9999))
	globals()['vcard_pending'].append(id)
	vcard_iq.setID(id)
	vcard_iq.addChild('vCard', {}, [], 'vcard-temp');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			nick = parameters.strip()
			if not nick in nicks:
				vcard_iq.setTo(nick)
			else:
				if GROUPCHATS[source[1]][nick]['ishere']==0:
					reply(type, source, u'а он тут? :-O')
					return				
				jid=source[1]+'/'+nick
				vcard_iq.setTo(jid)
	else:
		jid=source[1]+'/'+source[2]
		vcard_iq.setTo(jid)
		nick=''
	JCON.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick})
		

def handler_vcardget_answ(coze, res, type, source, nick):
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
			if not nick:
				reply(type,source,u'хехе, твой клиент ничего не знает про вкарды')
				return
			else:
				reply(type,source,u'хехе, его клиент ничего не знает про вкарды')
				return
		elif res.getType() == 'result':
			name,nickname,url,email,desc = '','','','',''
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:
				if not nick:
					reply(type,source,u'вкард заполни сначала')
					return
				else:
					reply(type,source,u'передай ему, чтобы он свой вкард сначала заполнил')
					return
			for p in props:
				if p.getName() == 'NICKNAME':
					nickname = p.getData()
				if p.getName() == 'FN':
					name = p.getData()				
				if p.getName() == 'URL':
					url = p.getData()
				if p.getName() == 'EMAIL':
					email = p.getData()
				if p.getName() == 'DESC':
					desc = p.getData()
			if nickname:
				if not nick:
					rep = u'про тебя я знаю следующее:\nnick: '+nickname
				else:
					rep = u'про '+nick+u' я знаю следующее:\nnick: '+nickname
			if not name=='':
				rep +='\nname: '+name				
			if not url=='':
				rep +='\nurl: '+url
			if not email=='':
				rep +=u'\nemail: '+email		
			if not desc=='':
				rep +=u'\nabout: '+desc
			if rep=='':
				rep = u'пустой вкард'
		else:
			rep = u'он зашифровался'
	else:
		rep = u'что-то никак...'
	reply(type, source, rep)



register_command_handler(handler_vcardget, 'визитка', ['мук','инфо','все'], 10, 'Показывает vCard указанного пользователя.', 'визитка [ник]', ['визитка guy','визитка'])
