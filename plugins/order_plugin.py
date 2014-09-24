#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  order_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

order_stats = {}
order_obscene_words = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог', u'fuck', u' fuck', u'pussy', u'cunt']
order_url_words = [u'www', u'wap', u'.net', u'http:']
order_add_words = [u'@con', u'conference.jabber', u'%s@con']
order_english_only_words = [u'а', u'о', u'е', u'и', u'я', u'д', u'أ', u'ه', u'ش', u'ذ', u'س', u'ث', u'د ', u'ق', u'ر', u'字母a', u'ü', u'字母i', u'אני', u'דואר', u'わたし', u'図書館', u'나', u'من'] 
AVIPES={}
AVSERVERS=['jabber.ru','xmpp.ru', 'jabbers.ru', 'xmpps.ru', 'qip.ru', 'talkonaut.com', 'jabbus.org', 'jabber.org','gtalk.com','jabber.cz','jabberon.ru','jabberid.org','linuxoids.net','jabber.kiev.ua','jabber.ufanet.ru','jabber.corbina.ru']

def order_unban_v(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_ban_v(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', u'Suspicious for the attack with wipe methode!')
	iq.addChild(node=query)
	JCON.send(iq)
		
def get_serv(serv):
	if serv.count('@'):
		serv=serv.split('@')[1]
	if serv.count('/'):
		serv=serv.split('/')[0]
	return serv		
		
def findPresenceItemV(node):
	for p in [x.getTag('item') for x in node.getTags('x',namespace='http://jabber.org/protocol/muc#user')]:
              if p != None:
                      return p
        return None


		
def avipe_prs(prs):
	ptype = prs.getType()
	if ptype == 'unavailable' and prs.getStatusCode() == '303':
		nick = prs.getNick()
		fromjid = prs.getFrom()
		groupchat = fromjid.getStripped()		
		afl=prs.getAffiliation()
		role=prs.getRole()
		avipe_join(groupchat, nick, afl, role)


def avipe_join(groupchat, nick, afl, role):		
	global AVIPES
	if not AVIPES.has_key(groupchat):
		return
	
	if afl != 'none':
		return
	jid = get_true_jid(groupchat+'/'+nick)		
	if not jid or jid.count('@localhost'):
		return
	
	global INFO	
	ttime=int(time.time())	
	if ttime - INFO['start'] < 60:	
		return
	
	if (ttime - AVIPES[groupchat]['ltime']) > 20:
		AVIPES[groupchat]['ltime']=ttime
		AVIPES[groupchat]['num']=0
		AVIPES[groupchat]['jids']=[jid]
		return
	AVIPES[groupchat]['num']+=1
	AVIPES[groupchat]['jids'].append(jid)
	joined=AVIPES[groupchat]['jids']
	
	global GROUPCHATS
	if len(joined) > 2:
		AVIPES[groupchat]['ltime']=ttime
		x=len(joined)
		if (get_serv(joined[x-2]) == get_serv(joined[x-1])) and (get_serv(joined[x-3]) == get_serv(joined[x-1])):    #and joined[x-2] != joined[x-1]:
			serv=get_serv(joined[x-2])
			if not serv in AVSERVERS:			
				node='<item affiliation="outcast" jid="'+serv+u'"><reason>Suspicious for the attack with wipe methode.</reason></item>'
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+JID+'/'+RESOURCE+'" id="ban1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)						
			node=''
			for nick in GROUPCHATS[groupchat].keys():
				if get_serv(get_true_jid(groupchat+'/'+nick)) == serv and GROUPCHATS[groupchat][nick]['ishere']:
					node+='<item role="none" nick="'+nick+u'"><reason>Suspicious for the attack with wipe methode.</reason></item>'
			if node:
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+JID+'/'+RESOURCE+'" id="kick1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)

			if not serv in AVSERVERS:
				for nick in GROUPCHATS[groupchat].keys():
					if user_level(groupchat+'/'+nick, groupchat) > 19:
						#if GROUPCHATS[groupchat][nick]['status'] in [u'online',u'chat',u'away']:
						msg(groupchat+'/'+nick, u'Warning! Server '+serv+u' is listed in the ban list!')

	if AVIPES[groupchat]['num'] > 4:
		order_ban_v(groupchat, jid)
		threading.Timer(60, order_unban_v,(groupchat, jid, )).start()
		

def avipe_call(type, source, parameters):
	global AVIPES
	PATH='dynamic/'+source[1]+'/antivipe.txt'
	parameters=parameters.strip().lower()
	if parameters:
		if check_file(source[1],'antivipe.txt'):
			if parameters=='on' or parameters=='1' or parameters==u'вкл':
				write_file(PATH, 'on')
				AVIPES[source[1]]={'ltime':0, 'num':0, 'jids': []}
				reply(type, source, u'Function antivipe is enable!')
			elif parameters=='off' or parameters=='0' or parameters==u'выкл':
				write_file(PATH, 'off')
				if AVIPES.has_key(source[1]):
					del AVIPES[source[1]]
				reply(type, source, u'Function antivipe is disable!')
			else:
				reply(type, source, u'Read help on command!')
	else:
		if not AVIPES.has_key(source[1]):
			reply(type, source, u'You have disabled the function antivipe!')
		else:
			reply(type, source, u'You have enabled the function antivipe!')


def avipe_init(groupchat):
	if check_file(groupchat,'antivipe.txt'):
		if not read_file('dynamic/'+groupchat+'/antivipe.txt')=='off':
			AVIPES[groupchat]={'ltime':0, 'num':0, 'jids': []}

	
		
register_presence_handler(avipe_prs)
register_join_handler(avipe_join)
register_command_handler(avipe_call, 'antivipe', ['all', 'admin'], 20, 'Enable/disable the function of protection against vipe attacks. Able to protect from the primitive and secondary attacks. Default is ON.', 'antivipe [<1/on/вкл/0/off/выкл>]', ['antivipe on','antivipe off'])
register_stage1_init(avipe_init)	




"""	
	global GROUPCHATS
	if len(joined) > 2:
		x=len(joined)
		if (get_serv(joined[x-2]) == get_serv(joined[x-1])) and (get_serv(joined[x-3]) == get_serv(joined[x-1])):                   #and joined[x-2] != joined[x-1]:
			serv=get_serv(joined[x-2])
			if not serv in AVSERVERS:			
				node='<item affiliation="outcast" jid="'+serv+u'"><reason>Подозрение на вайп атаку.</reason></item>'
				for nick in GROUPCHATS[groupchat].keys():
					if get_serv(get_true_jid(groupchat+'/'+nick)) == serv and GROUPCHATS[groupchat][nick]['ishere']:
						print nick,
						node+='<item role="none" nick="'+nick+u'"><reason>Подозрение на вайп атаку.</reason></item>'				
				
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+USERNAME+'@'+SERVER+'/'+RESOURCE+'" id="ban1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)						
				for nick in GROUPCHATS[groupchat].keys():
					if user_level(groupchat+'/'+nick, groupchat) > 19:
						if GROUPCHATS[groupchat][nick]['status'] in [u'online',u'chat',u'away']:
							msg(groupchat+'/'+nick, u'Внимание! Сервер '+serv+u' занесен в бан лист!')
"""


def order_check_obscene_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in order_obscene_words:
		if body.count(x):
			return True
	return False

def order_check_add_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in order_add_words:
		if body.count(x):
			return True
	return False

def order_check_english_only_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in order_english_only_words:
		if body.count(x):
			return True
	return False

def order_check_url_words(body):
        body=body.lower()
        body=u' '+body+u' '
        for x in order_url_words:
                if body.count(x):
                        return True
        return False

def order_check_time_flood(gch, jid, nick):
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and time.time()-lastmsg<=2.2:
		order_stats[gch][jid]['msg']+=1
		if order_stats[gch][jid]['msg']>3:
			order_stats[gch][jid]['msg']=0
			order_kick(gch, nick, u'Too rapidly you send')
			return True
		return False
	
def order_check_len_flood(mlen, body, gch, jid, nick):			
	if len(body)>mlen:
		order_kick(gch, nick, u'flood')
		return True
	return False
				
def order_check_obscene(body, gch, jid, nick):
	if order_check_obscene_words(body):
		order_kick(gch, nick, u'obscene word')
		return True
	return False

def order_check_obscene2(body, gch, jid, nick):
	if order_check_obscene_words(body):
                order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
                order_kick(gch, nick, u'your voice has been revoked for swearing wait for a moderator to decide to grant it upon entering')
	        return True
	return False
		
def order_check_caps(body, gch, jid, nick):
	ccnt=0
	nicks = GROUPCHATS[gch].keys()
	for x in nicks:
		if body.count(x):
			body=body.replace(x,'')
	for x in [x for x in body.replace(' ', '')]:
		if x.isupper():
			ccnt+=1
	if ccnt>=len(body)/2 and ccnt>9:
		order_kick(gch, nick, u'capsa!!!')
		return True
	return False

def order_check_url(body, gch, jid, nick):
	if order_check_url_words(body):
		order_kick(gch, nick, u'url')
		return True
	return False

def order_check_add(body, gch, jid, nick):
	if order_check_add_words(body):
		order_kick(gch, nick, u'advertising')
		return True
	return False        	

def order_check_english_only(body, gch, jid, nick):
        if order_check_english_only_words(body):
                order_kick(gch, nick, u'english only')
                return True
        return False              

def order_check_like(body, gch, jid, nick):		
	lcnt=0
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and order_stats[gch][jid]['msgbody']:
		if time.time()-lastmsg>60:
			order_stats[gch][jid]['msgbody']=body.split()
		else:
			for x in order_stats[gch][jid]['msgbody']:
				for y in body.split():
					if x==y:
						lcnt+=1
			if lcnt:
				lensrcmsgbody=len(body.split())
				lenoldmsgbody=len(order_stats[gch][jid]['msgbody'])
				avg=(lensrcmsgbody+lenoldmsgbody/2)/2
				if lcnt>avg:
					order_stats[gch][jid]['msg']+=1
					if order_stats[gch][jid]['msg']>=2:
						order_stats[gch][jid]['msg']=0
						order_kick(gch, nick, u'Messages are too similar')
						return True
			order_stats[gch][jid]['msgbody']=body.split()
	else:
		order_stats[gch][jid]['msgbody']=body.split()
	return False

####################################################################################################

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

def handler_order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)
		
def order_visitor(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
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
	
def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_check_idle():
	for gch in GROUPCHATS.keys():
		if GCHCFGS[gch]['filt']['idle']['cond']==1:
			timee=GCHCFGS[gch]['filt']['idle']['time']
			now=time.time()
			for nick in GROUPCHATS[gch].keys():
				if GROUPCHATS[gch][nick]['ishere']==1:
					if user_level(gch+'/'+nick,gch)<11:
						idle=now-GROUPCHATS[gch][nick]['idle']
						if idle > timee:
							order_kick(gch, nick, u'Silence more '+timeElapsed(idle))
	threading.Timer(120,order_check_idle).start()
	
####################################################################################################

def handler_order_message(type, source, body):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS.keys() and user_level(source,groupchat)<11:
		if get_bot_nick(groupchat)!=nick:
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats and jid in order_stats[groupchat]:
				if GCHCFGS[groupchat]['filt']['time']==1:
					if order_check_time_flood(groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['len']==1:
					if order_check_len_flood(900, body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['obscene']==1:
					if order_check_obscene(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['obscene2']==1:
					if order_check_obscene2(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['url']==1:
					if order_check_url(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['add']==1:
					if order_check_add(body, groupchat, jid, nick):	return
                                if GCHCFGS[groupchat]['filt']['english_only']==1:
					if order_check_english_only(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['caps']==1:
					if order_check_caps(body, groupchat, jid, nick):	return
				if GCHCFGS[groupchat]['filt']['like']==1:
					if order_check_like(body, groupchat, jid, nick):	return
				order_stats[groupchat][jid]['msgtime']=time.time()
				
def handler_order_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		now = time.time()
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		if jid in order_stats[groupchat].keys():
			if order_stats[groupchat][jid]['devoice']['cnd']==1:
				if now-order_stats[groupchat][jid]['devoice']['time']>300:
					order_stats[groupchat][jid]['devoice']['cnd']=0
				else:
					order_visitor(groupchat, nick, u'The vote is removed for the previous infringements')

			if GCHCFGS[groupchat]['filt']['kicks']['cond']==1:
				kcnt=GCHCFGS[groupchat]['filt']['kicks']['cnt']
				if order_stats[groupchat][jid]['kicks']>kcnt:
					order_ban(groupchat, nick, u'too many kicks')
					return

			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()	
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
					if order_stats[groupchat][jid]['prs']['fly']>4:
						order_stats[groupchat][jid]['prs']['fly']=0
						fmode=GCHCFGS[groupchat]['filt']['fly']['mode']
						ftime=GCHCFGS[groupchat]['filt']['fly']['time']
						if fmode=='ban':
							order_ban(groupchat, nick, u'Will suffice to fly')
							time.sleep(ftime)
							order_unban(groupchat, jid)
						else:
							order_kick(groupchat, nick, u'Will suffice to fly')
							return
				else:
					order_stats[groupchat][jid]['prs']['fly']=0
			
			if GCHCFGS[groupchat]['filt']['obscene']==1:		
				if order_check_obscene(nick, groupchat, jid, nick):	return

			if GCHCFGS[groupchat]['filt']['obscene2']==1:		
				if order_check_obscene2(nick, groupchat, jid, nick):	return

			if GCHCFGS[groupchat]['filt']['url']==1:		
				if order_check_url(nick, groupchat, jid, nick):	return

			if GCHCFGS[groupchat]['filt']['add']==1:		
				if order_check_add(nick, groupchat, jid, nick):	return	

                        if GCHCFGS[groupchat]['filt']['english_only']==1:		
				if order_check_english_only(nick, groupchat, jid, nick): return

			if GCHCFGS[groupchat]['filt']['len']==1:	
				if order_check_len_flood(20, nick, groupchat, jid, nick):	return
			
		elif nick in GROUPCHATS[groupchat]:
			order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}

	elif groupchat in order_stats and jid in order_stats[groupchat]:
		del order_stats[groupchat][jid]
	else:
		pass			

def handler_order_presence(prs):
	ptype = prs.getType()
	if ptype=='unavailable' or ptype=='error':
		return
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)
	
	if groupchat in order_stats and jid in order_stats[groupchat]:
		if item['affiliation'] in ['member','admin','owner']:
			del order_stats[groupchat][jid]
			return
	else:
		if item['affiliation']=='none':
			order_stats[groupchat][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': None, 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0}
	
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			now = time.time()
			if now-GROUPCHATS[groupchat][nick]['joined']>1:
				if item['role']=='participant':
					order_stats[groupchat][jid]['devoice']['cnd']=0
				lastprs=order_stats[groupchat][jid]['prstime']['status']
				order_stats[groupchat][jid]['prstime']['status']=now

				if GCHCFGS[groupchat]['filt']['presence']==1:
					if now-lastprs>300:
						order_stats[groupchat][jid]['prs']['status']=0
					else:
						order_stats[groupchat][jid]['prs']['status']+=1
						if order_stats[groupchat][jid]['prs']['status']>5:
							order_stats[groupchat][jid]['prs']['status']=0
							order_kick(groupchat, nick, u'presence flood')
							return

				if GCHCFGS[groupchat]['filt']['obscene']==1:		
					if order_check_obscene(nick, groupchat, jid, nick):	return

				if GCHCFGS[groupchat]['filt']['obscene2']==1:		
					if order_check_obscene2(nick, groupchat, jid, nick):	return

				if GCHCFGS[groupchat]['filt']['url']==1:		
					if order_check_url(nick, groupchat, jid, nick):	return

				if GCHCFGS[groupchat]['filt']['add']==1:		
					if order_check_add(nick, groupchat, jid, nick):	return		
				
				if GCHCFGS[groupchat]['filt']['prsstlen']==1 and stmsg:
					if order_check_len_flood(200, nick, groupchat, jid, nick):	return

def handler_order_leave(groupchat, nick, reason, code):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			if GCHCFGS[groupchat]['filt']['presence']==1:
				if reason=='Replaced by new connection':
					return
				if code:
					if code=='307': # kick
						order_stats[groupchat][jid]['kicks']+=1
						return
					elif code=='301': # ban
						del order_stats[groupchat][jid]
						return
					elif code=='407': # members-only
						return
			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				now = time.time()
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
				else:
					order_stats[groupchat][jid]['prs']['fly']=0

######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		parameters=parameters.split()
		if len(parameters)<2:
			reply(type,source,u'invalid')
			return
		if GCHCFGS[source[1]].has_key('filt'):
			if parameters[0]=='time':
				if parameters[1]=='0':
					reply(type,source,u'time filter is off')
					GCHCFGS[source[1]]['filt']['time']=0
				elif parameters[1]=='1':
					reply(type,source,u'time filter is on')
					GCHCFGS[source[1]]['filt']['time']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='presence':
				if parameters[1]=='0':
					reply(type,source,u'presence filter is off')
					GCHCFGS[source[1]]['filt']['presence']=0
				elif parameters[1]=='1':
					reply(type,source,u'presence filter is on')
					GCHCFGS[source[1]]['filt']['presence']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='len':
				if parameters[1]=='0':
					reply(type,source,u'len filter is off')
					GCHCFGS[source[1]]['filt']['len']=0
				elif parameters[1]=='1':
					reply(type,source,u'len filter is on')
					GCHCFGS[source[1]]['filt']['len']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='like':
				if parameters[1]=='0':
					reply(type,source,u'like filter is off')
					GCHCFGS[source[1]]['filt']['like']=0
				elif parameters[1]=='1':
					reply(type,source,u'like filter is on')
					GCHCFGS[source[1]]['filt']['like']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='caps':
				if parameters[1]=='0':
					reply(type,source,u'CAPSA filter is off')
					GCHCFGS[source[1]]['filt']['caps']=0
				elif parameters[1]=='1':
					reply(type,source,u'CAPSA filter is on')
					GCHCFGS[source[1]]['filt']['caps']=1
				else:
					reply(type,source,u'invalid')	
			elif parameters[0]=='prsstlen':
				if parameters[1]=='0':
					reply(type,source,u'prsstlen filter is off')
					GCHCFGS[source[1]]['filt']['prsstlen']=0
				elif parameters[1]=='1':
					reply(type,source,u'prsstlen filter is on')
					GCHCFGS[source[1]]['filt']['prsstlen']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='obscene':
				if parameters[1]=='0':
					reply(type,source,u'obscene filter is off')
					GCHCFGS[source[1]]['filt']['obscene']=0
				elif parameters[1]=='1':
					reply(type,source,u'obscene filter is on')
					GCHCFGS[source[1]]['filt']['obscene']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='obscene2':
				if parameters[1]=='0':
					reply(type,source,u'obscene2 filter is off')
					GCHCFGS[source[1]]['filt']['obscene2']=0
				elif parameters[1]=='1':
					reply(type,source,u'obscene2 filter is on')
					GCHCFGS[source[1]]['filt']['obscene2']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='url':
				if parameters[1]=='0':
					reply(type,source,u'url filter is off')
					GCHCFGS[source[1]]['filt']['url']=0
				elif parameters[1]=='1':
					reply(type,source,u'url filter is on')
					GCHCFGS[source[1]]['filt']['url']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='add':
				if parameters[1]=='0':
					reply(type,source,u'add filter is off')
					GCHCFGS[source[1]]['filt']['add']=0
				elif parameters[1]=='1':
					reply(type,source,u'add filter is on')
					GCHCFGS[source[1]]['filt']['add']=1
				else:
					reply(type,source,u'invalid')		
                        elif parameters[0]=='english_only':
				if parameters[1]=='0':
					reply(type,source,u'english_only filter is off')
					GCHCFGS[source[1]]['filt']['english_only']=0
				elif parameters[1]=='1':
					reply(type,source,u'english_only filter is on')
					GCHCFGS[source[1]]['filt']['english_only']=1
				else:
					reply(type,source,u'invalid')	
			elif parameters[0]=='fly':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invaled syntax')
					if int(parameters[2]) in xrange(0,121):
						reply(type,source,u'разморозка it is established on '+parameters[2]+u' Seconds')
						GCHCFGS[source[1]]['filt']['fly']['time']=int(parameters[2])	
					else:
						reply(type,source,u'No more than two minutes (120 Seconds)')
				elif parameters[1]=='mode':
					if parameters[2] in ['kick','ban']:
						if parameters[2] == 'ban':
							reply(type,source,u'For flights i shall ban')
							GCHCFGS[source[1]]['filt']['fly']['mode']='ban'
						else:
							reply(type,source,u'For flights i shall kick')
							GCHCFGS[source[1]]['filt']['fly']['mode']='kick'	
					else:
						reply(type,source,u'invaled')		
				elif parameters[1]=='0':
					reply(type,source,u'fly filter is off')
					GCHCFGS[source[1]]['filt']['fly']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'fly filter is on')
					GCHCFGS[source[1]]['filt']['fly']['cond']=1
				else:
					reply(type,source,u'invalid')
			elif parameters[0]=='kicks':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invalid')
					if int(parameters[2]) in xrange(2,10):
						reply(type,source,u'aban after '+parameters[2]+u' kickoff')
						GCHCFGS[source[1]]['filt']['kicks']['cnt']=int(parameters[2])	
					else:
						reply(type,source,u'from 2 to 10 kickoffs')
				elif parameters[1]=='0':
					reply(type,source,u'kicks filter is off')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'kicks filter is on')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=1
				else:
					reply(type,source,u'invaled')
			elif parameters[0]=='idle':
				if parameters[1]=='time':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'invaled')			
					reply(type,source,u'kick For silence after '+parameters[2]+u' Seconds ('+timeElapsed(int(parameters[2]))+u')')
					GCHCFGS[source[1]]['filt']['idle']['time']=int(parameters[2])
				elif parameters[1]=='0':
					reply(type,source,u'idle filter is off')
					GCHCFGS[source[1]]['filt']['idle']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'idle filter is on')
					GCHCFGS[source[1]]['filt']['idle']['cond']=1
			else:
				reply(type,source,u'invaled')
				return					
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		else:
			reply(type,source,u'There was something strange, ask the administrator of a bot')
	else:
		rep,foff,fon=u'',[],[]
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		flen=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		caps=GCHCFGS[source[1]]['filt']['caps']
		prsstlen=GCHCFGS[source[1]]['filt']['prsstlen']
		obscene=GCHCFGS[source[1]]['filt']['obscene']
		obscene2=GCHCFGS[source[1]]['filt']['obscene2']
		url=GCHCFGS[source[1]]['filt']['url']
		add=GCHCFGS[source[1]]['filt']['add']
                english_only=GCHCFGS[source[1]]['filt']['english_only']
		fly=GCHCFGS[source[1]]['filt']['fly']['cond']
		flytime=str(GCHCFGS[source[1]]['filt']['fly']['time'])
		flymode=GCHCFGS[source[1]]['filt']['fly']['mode']
		kicks=GCHCFGS[source[1]]['filt']['kicks']['cond']
		kickscnt=str(GCHCFGS[source[1]]['filt']['kicks']['cnt'])
		idle=GCHCFGS[source[1]]['filt']['idle']['cond']
		idletime=GCHCFGS[source[1]]['filt']['idle']['time']
		if time:
			fon.append(u'time')
		else:
			foff.append(u'time')
		if prs:
			fon.append(u'presence')
		else:
			foff.append(u'presence')
		if flen:
			fon.append(u'len')
		else:
			foff.append(u'len')
		if like:
			fon.append(u'like')
		else:
			foff.append(u'like')
		if caps:
			fon.append(u'CAPSA')
		else:
			foff.append(u'CAPSA')
		if prsstlen:
			fon.append(u'prsstlen')
		else:
			foff.append(u'prsstlen')
		if obscene:
			fon.append(u'obscene')
		else:
			foff.append(u'obscene')
		if obscene2:
			fon.append(u'obscene2')
		else:
			foff.append(u'obscene2')
		if url:
			fon.append(u'url')
		else:
			foff.append(u'url')
		if add:
			fon.append(u'add')
		else:
			foff.append(u'add')	
                if english_only:
			fon.append(u'english_only')
		else:
			foff.append(u'english_only')	
		if fly:
			fon.append(u'fly (Mode '+flymode+u', The timer '+flytime+u' Seconds)')
		else:
			foff.append(u'fly')
		if kicks:
			fon.append(u'ban after '+kickscnt+u' kicks')
		else:
			foff.append(u'kicks')
		if idle:
			fon.append(u'idle '+str(idletime)+u' Seconds ('+timeElapsed(idletime)+u')')
		else:
			foff.append(u'idle')
		fon=u', '.join(fon)
		foff=u', '.join(foff)
		if fon:
			rep+=u'ARE INCLUDED\n'+fon+u'\n\n'
		if foff:
			rep+=u'ARE SWITCHED OFF\n'+foff
		reply(type,source,rep.strip())


def get_order_cfg(gch):
	if not 'filt' in GCHCFGS[gch]:
		GCHCFGS[gch]['filt']={}		
	for x in ['time','presence','len','like','caps','prsstlen','obscene','obscene2','url','add','english_only','kicks','fly','excess','idle']:
		if x == 'excess':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'mode': 'kick'}
			continue		
		if x == 'kicks':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'cnt': 2}
			continue
		if x == 'fly':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'mode': 'ban', 'time': 60}
			continue
		if x == 'idle':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'time': 3600}
			continue
		if not x in GCHCFGS[gch]['filt']:
			GCHCFGS[gch]['filt'][x]=1
			

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['admin','muc','all'], 20, 'Includes or disconnects the certain filters for conference.\ntime - The time filter\nlen - The quantitative filter\npresence - The filter presence\nlike - The filter of identical messages\nadd - the advertising of conference filter\ncaps - The filter CAPS (CAPITAL LETTERS)\nprsstlen - The filter of long status messages\nobscene - filtering of bad words\nenglish_only - filter for english only!\nurl - the filter for url,websites= www,wap\nfly - The filter of flights (Frequent inputs/Outputs in conference), Has two modes ban and kick, The timer from 0 to 120 seconds\nkicks - ban after a certain amount of kicks, Parameter cnt - quantity kick off from 1 up to 10\nidle - kick for silence in the general chat after N seconds, parameter time - in seconds for operation', 'filt [filter] [Mode] [state]', ['filt smile 1', 'filt len 0','filt fly mode ban'])
register_command_handler(handler_order_kick, 'kick', ['admin','muc','all'], 15, 'kick person out the room u can also give the reason for kick', 'kick <nick> <reason>', ['kick joe','kick joe flood'])
register_command_handler(order_visitor, 'visitor', ['admin','muc','all'], 20, 'make someone a visitor', 'visitor <nick>', ['visitor joe','visitor sam'])
register_command_handler(order_ban, 'ban', ['admin','muc','all'], 20, 'ban asshole from entering the room can also add a reason', 'ban <nick> <reason>', ['ban benny','ban benny asshole'])
register_command_handler(order_unban, 'unban', ['admin','muc','all'], 20, 'to unban jid', 'unban <jid>', ['unban joe@jabber.ru'])
register_command_handler(order_ban, 'aban', ['admin','muc','all'], 20, 'aban <jid> ,') 
                         
register_stage1_init(get_order_cfg)
register_stage2_init(order_check_idle)
