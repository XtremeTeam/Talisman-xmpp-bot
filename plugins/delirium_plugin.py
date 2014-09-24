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

poke_nicks={}

def handler_poke(type, source, parameters):
	if type=='private':
		reply(type,source,u':-P')
		return
	groupchat = source[1]
	if parameters:
		if parameters==u'last10':
			cnt=0
			rep=''
			nicks = set()
			for x in [poke_nicks[source[1]] for x in poke_nicks]:
				nicks = nicks | set(x)
			for x in nicks:
				cnt=cnt+1
				rep += str(cnt)+u') '+x+u'\n'
			reply('private',source,rep[:-1])
			return
		if not poke_nicks.has_key(source[1]):
			poke_nicks[source[1]]=source[1]
			poke_nicks[source[1]]=[]
		if len(poke_nicks[source[1]])==10:
			poke_nicks[source[1]]=[]
		else:
			poke_nicks[source[1]].append(source[2])
		if not parameters == get_bot_nick(source[1]):
			if parameters in GROUPCHATS[source[1]]:
				pokes=[]
				pokes.extend(poke_work(source[1]))
				pokes.extend(eval(read_file('static/delirium.txt'))['poke'])
				rep = random.choice(pokes)
				msg(source[1],u'/me '+rep % parameters)
			else:
				reply(type, source, u'And it here? :-O')
		else:
			reply(type, source, u'Very clever, yes? ]:->')	
	else:
		reply(type, source, u'who? :D')
		
def handler_poke_add(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
	if not parameters.count('%s'):
		reply(type, source, u'i am not seeing %s')
		return
	res=poke_work(source[1],1,parameters)
	if res:
		reply(type, source, u'added')
	else:
		reply(type, source, u'impossible')
		
def handler_poke_del(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
	if parameters=='*':
		parameters='0'
	else:
		try:
			int(parameters)
		except:
			reply(type,source,u'invalid')
	res=poke_work(source[1],2,parameters)
	if res:
		reply(type, source, u'removed')
	else:
		reply(type, source, u'Such is not present')
		
def handler_poke_list(type, source, parameters):
	rep,res=u'',poke_work(source[1],3)
	if res:
		res=sorted(res.items(),lambda x,y: int(x[0]) - int(y[0]))
		for num,phrase in res:
			rep+=num+u') '+phrase+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'There are no user phrases')
		
def handler_test(type, source, parameters):
	reply(type,source,u'passed')
	
def handler_clean_conf(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		for x in range(1, 25):
			msg(source[1], '')
			time.sleep(1.3)
		reply(type,source,u'done')
		
def handler_afools_control(type, source, parameters):
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'invaled')
		if int(parameters)>1:
			reply(type,source,u'invaled')
		if parameters=="1":
			GCHCFGS[source[1]]['afools']=1
			reply(type,source,u' are included')
		else:
			GCHCFGS[source[1]]['afools']=0
			reply(type,source,u'jokes disconnected')			
	else:
		if GCHCFGS[source[1]]['afools']==1:
			reply(type,source,u'jokes are included')
		else:
			reply(type,source,u'jokes are disabled')
	
			
def get_afools_state(gch):
	if not 'afools' in GCHCFGS[gch]:
		GCHCFGS[gch]['afools']=1
		
def poke_work(gch,action=None,phrase=None):
	DBPATH='dynamic/'+gch+'/delirium.txt'
	if check_file(gch,'delirium.txt'):
		pokedb = eval(read_file(DBPATH))
		if action==1:
			for x in range(1, 21):
				if str(x) in pokedb.keys():
					continue
				else:
					pokedb[str(x)]=phrase
					write_file(DBPATH, str(pokedb))
					return True
			return False
		elif action==2:
			if phrase=='0':
				pokedb.clear()
				write_file(DBPATH, str(pokedb))
				return True
			else:
				try:
					del pokedb[phrase]
					write_file(DBPATH, str(pokedb))
					return True
				except:
					return False
		elif action==3:
			return pokedb
		else:
			return pokedb.values()
	else:
		return None
		
def remix_string(parameters):
	remixed=[]
	for word in parameters.split():
		tmp=[]
		if len(word)<=1:
			remixed.append(word)
			continue
		elif len(word)==2:
			tmp=list(word)
			random.shuffle(tmp)
			remixed.append(u''.join(tmp))
		elif len(word)==3:
			tmp1=list(word[1:])
			tmp2=list(word[:-1])
			tmp=random.choice([tmp1,tmp2])
			if tmp==tmp1:
				random.shuffle(tmp)
				remixed.append(word[0]+u''.join(tmp))
			else:
				random.shuffle(tmp)
				remixed.append(u''.join(tmp)+word[-1])					
		elif len(word)>=4:
			tmp=list(word[1:-1])
			random.shuffle(tmp)
			remixed.append(word[0]+u''.join(tmp)+word[-1])
	return u' '.join(remixed)

def handler_kick_ass(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		if parameters:
			rep = '>:D'
			splitdata = string.split(parameters)
			if splitdata[0]==u'>:D':
				for x in range(0, int(splitdata[1])):
					for y in range(0, int(splitdata[2])):
						rep += u'>:D'
					msg(source[1], rep)
					rep = 'asshole '
					time.sleep(0.5)
			else:
				for x in range(0, int(splitdata[1])):
					for y in range(0, int(splitdata[2])):
						rep += u'asshole!!!!!! >:D '
					msg(source[1]+'/'+splitdata[0], rep)
					rep = ':) '
					time.sleep(0.5)
 
def handler_english(type, source, parameters):
        reply(type, source,u'english please')

def handler_hi(type, source, parameters):
	reply(type,source,u'hi :)')

def handler_8ball(type, source, body):
	replies = ['no', 'my senses tells me no', 'probably not', 'yes', 'maybe', 'my senses says yes', 'probably', 'i cant say now', 'definitely', 'ask again', 'uhm...il tell you later']
	reply = random.choice(replies)
	smsg(type, source, reply)

register_command_handler(handler_poke, 'poke', ['fun','muc','all'], 0, 'pokes the user. Forces it to pay attention to you/in chat.\nlast10', 'poke <nick>|<Parameter>', ['poke qwerty','poke + пришиб %s','poke - 2','poke *'])
register_command_handler(handler_poke_add, 'pokeadd', ['fun','muc','all'], 20, 'To add the user phrase. Variable %s for placing of the nick (Obligatory parameter). The phrase should be written from the third party, т.к. It will be used in the form of "/me Your phrase". max è«½-in the user phrases - 20.', 'pokeadd <Phrase>', ['pokeadd kisses %s'])
register_command_handler(handler_poke_del, 'pokedel', ['fun','muc','all'], 20, 'To remove the user phrase. write the number of the phrase you want to delete. The numbered list is given out with a command "pokelist". To remove all phrases it is possible by means of a symbol "*" Instead of number of a phrase.', 'pokedel <Number>', ['pokedel 5','pokedel *'])
register_command_handler(handler_poke_list, 'pokelist', ['fun','muc','all'], 20, 'Shows the numbered list of all user phrases.', 'pokelist', ['pokelist'])
register_command_handler(handler_test, 'test', ['fun','muc','all'], 0, 'Stupidly answers passed.', 'test', ['test'])
register_command_handler(handler_test, 'test', ['fun','muc','all'], 0, 'Stupidly answers passed.', 'test', ['test'])
register_command_handler(handler_clean_conf, 'clean', ['fun','muc','all'], 15, 'cleaning of conference (Considers up to 20).', 'clean', ['clean'])
register_command_handler(handler_afools_control, 'afools', ['fun','muc','all'], 30, 'Switches on and off jokes of bot for which it to a plenty substitutes(It always executes a command!) The standard answer of a command.', 'afools <1|0>', ['afools 1','afools 0'])
register_command_handler(handler_english, 'привет', ['fun','muc','all'], 0, 'replies "english please".you can diconnect this command')
register_command_handler(handler_hi, 'hi', ['fun','muc','all'], 0, 'let bot say hi to users.if its annoying simply turn it off with "commoff hi".')
register_command_handler(handler_8ball, '8ball', ['fun','muc','all'], 0, 'ask 8ball a question and it will answer.', '8ball <question>', ['8ball am i sick?'])

#  listed below command handler are not recommended
register_command_handler(handler_kick_ass, 'spam', ['fun','superadmin','muc','all'], 21, 'Spam of JID in a conference by the indicated amount of reports with smiles, amount of which is determined the the third parameter. If the first parameter is smile ( :) ), by the spam amount of reporting from the second parameter, adding to every report the amount of smiles from the third parameter.', 'spam [nick] [amount] [amount]', ['spam Pily 100 200','spam :) 50 200'])


register_stage1_init(get_afools_state)
