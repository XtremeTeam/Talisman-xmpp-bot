#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  zpyaiml_plugin.py

#created by planb(planb@talkonaut.com)

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

import aiml
import string
from string import *
k = aiml.Kernel()

def chat_pyaiml(type, source, body):
    k.learn("std-startup.xml")
    reply = k.respond(body.replace(get_bot_nick(source[1])+':','').strip())
    k.respond("load aiml b")
    smsg(type, source, reply)
    
def handler_pyaiml(type, source, body):
    if type == 'private':
		if not COMMANDS.has_key(string.split(body)[0]):
                        chat_pyaiml(type, source, body)    

    if type == 'public' and get_bot_nick(source[1])!=source[2] and source[2]!='' and re.search('^'+get_bot_nick(source[1])+':',body)!=None:
                        reply = k.respond(body.replace(get_bot_nick(source[1])+':','').strip())
		        chat_pyaiml(type, source, body)
	

register_message_handler(handler_pyaiml)
