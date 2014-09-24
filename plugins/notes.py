# coding: utf-8

# notes.py
# Initial Copyright (с) ???
# Modification Copyright (c) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

NOTE_FILE = "notepad.dat"

def openUserNotes():
	path = getConfigPath(NOTE_FILE)
	return database.DataBase(path)

def add_user_notes(msgType, conference, nick, param):
	notes = openUserNotes()
	truejid = getTrueJID(conference, nick)
	if truejid not in notes:
		notes[truejid] = []
	text = u"%s\n%s" % (time.strftime("[%d.%m.%Y, %H:%M]"), param)
	notes[truejid].append(text)
	notes.save()
	sendMsg(msgType, conference, nick, u"Записала")

def del_user_notes(msgType, conference, nick, param):
	notes = openUserNotes()
	truejid = getTrueJID(conference, nick)
	if truejid in notes:
		try:
			param = int(param) - 1
			if param >= 0:
				del notes[truejid][param]
				if not notes[truejid]:
					del notes[truejid]
				notes.save()
				sendMsg(msgType, conference, nick, u"Удалила")
			else:
				raise IndexError
		except ValueError:
			sendMsg(msgType, conference, nick, u"Для удаления нужно указать номер заметки!")
		except IndexError:
			sendMsg(msgType, conference, nick, u"Нет такой заметки")
	else:
		sendMsg(msgType, conference, nick, u"В твоём блокноте пусто")

def show_user_notes(msgType, conference, nick, param):
	notes = openUserNotes()
	truejid = getTrueJID(conference, nick)
	if param == u"сброс":
		if truejid in notes:
			del notes[truejid]
			notes.save()
			sendMsg(msgType, conference, nick, u"Удалила")
		else:
			sendMsg(msgType, conference, nick, u"А у тебя и так ничего нет :P")
	elif not param:
		if truejid in notes:
			elements = [u"%d) %s" % (i + 1, note) for i, note in enumerate(notes[truejid])]
			if protocol.TYPE_PUBLIC == msgType:
				sendMsg(msgType, conference, nick, u"Ушли")
			message = u"Твои заметки:\n%s" % ("\n".join(elements))
			sendMsg(protocol.TYPE_PRIVATE, conference, nick, message)
		else:
			sendMsg(msgType, conference, nick, u"В твоём блокноте пусто")
			
register_command_handler(handler_show_user_notes, 'notes', ['','muc','all'], 10, 'Shows the notes added', 'notes []', ['', '', ''])
register_command_handler(Handler_add_user_notes, 'notes+', ['','muc','all'], 10, '')
register_command_handler(handler_del_user_notes, 'notes-', ['','muc','all'], 10, '', '')