__author__ = 'Johan Hoiness'

import sys
import os
import random
import time
import string
import connection
from time import strftime
import ceq
import json, urllib2
import thread

args = sys.argv

req_files = ['filegen.py', 'connection.py', 'commands.py', 'general.py', 'automatics.py']
for filename in req_files:
	if os.path.exists(filename) == False:
		print "Required file \"{}\" not found. Make sure you have acquired all files.".format(filename)
		sys.exit(1)


import filegen


if os.path.exists('config.py') == False:
	print 'No configuration-file found. Generating config.py'
	filegen.gen_config()
	os.execl(args[0], '')
if os.path.exists('revar.py') == False:
	print 'No reconfigurable file found. Generating revar.py'
	filegen.gen_revar()
	os.execl(args[0], '')


import config
import revar
import filegen
import commands
import general
import automatics

if not revar.channels:
	revar.channels = config.channel.replace(', ', ',').replace(' ', ',').split(',')


if len(args) > 1:
	if args[1].lower() == 'reconfig' or args[1].lower() == 'config':
		answr = raw_input("This will have you regenerate the configuration file and all old configurations will be lost.\nAre you sure you want to do this?(y/n) ")
		while answr.lower() != 'y' or answr.lower() != 'n':
			answr = raw_input("You must use the letters Y or N to answer: ")
		if answr.lower() == 'y':
			filegen.gen_config()
			sys.exit(0)
		if answr.lower() == 'n':
			sys.exit(0)
	elif args[1].lower() == 'help':
		print "Usage: python alison.py <help | reconfig | >"
		sys.exit(0)
	else:
		print "Flag not recognized."
		sys.exit(1)


def connect(server, port):
	print "Connecting to {} with port {}.".format(server, port)
	s = connection.s
	readbuffer = ''
	try:
		s.connect((server, port))
	except BaseException as exc:
		print 'Failed to connect: ' + str(exc)
		sys.exit(1)
	s.send("PASS %s\n" % config.password)
	s.send("USER %s %s %s :%s\n" % (config.bot_username, config.bot_hostname, config.bot_servername, config.bot_realname))
	s.send("NICK %s\n" % revar.bot_nick)
	mode_found = False

	while not mode_found:
		readbuffer = readbuffer + s.recv(2048)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for rline in temp:
			rline = string.rstrip(rline)
			rline = string.split(rline)
			g = general
			if rline[0] == "PING":
				g.ssend("PONG %s\r" % rline[1])

			if rline[1] == '433':
				if revar.bot_nick.lower() != config.bot_nick2.lower():
					revar.bot_nick = config.bot_nick2
				else:
					revar.bot_nick += '_'
				g.ssend('NICK %s' % revar.bot_nick)

			if len(rline) > 2 and rline[1] == '391':
				revar.bot_nick = rline[2]

			if len(rline) > 2 and rline[1].lower() == 'join':
				if not rline[2].lower() in revar.channels:
					revar.channels.append(rline[2].lower())

			if len(rline) > 2 and rline[1].lower() == 'part':
				if rline[2].lower() in revar.channels:
					try:
						revar.channels.append(rline[2].lower())
					except:
						pass

			if rline[1] == 'MODE':
				mode_found = True
				g.ssend('JOIN %s' % ','.join(revar.channels))


def server_responses(rline):
	g = general

	if rline[0] == "PING":
		g.ssend("PONG %s\r" % rline[1])
		return True

	if rline[1] == '433':
		if revar.bot_nick.lower() != config.bot_nick2.lower():
			revar.bot_nick = config.bot_nick2
		else:
			revar.bot_nick += '_'
		g.ssend('NICK %s' % revar.bot_nick)
		return True

	if len(rline) > 2 and rline[1] == '391':
		revar.bot_nick = rline[2]
		return True

	if len(rline) > 2 and rline[1].lower() == 'join':
		if not rline[2].lower() in revar.channels:
			revar.channels.append(rline[2].lower())
		return True

	if len(rline) > 2 and rline[1].lower() == 'part':
		if rline[2].lower() in revar.channels:
			try:
				revar.channels.append(rline[2].lower())
			except:
				pass
		return True
	if len(rline) > 3 and rline[1] == '319' and rline[2].lower() == revar.bot_nick.lower():
		revar.channels = ' '.join(rline[4:])[1:].replace('+', '').replace('@', '').lower().split()
		return True
	if len(rline) > 2 and rline[1] == '391':
		revar.bot_nick = rline[2]
		return True
	return False


def find_imdb_link(chanq, msg):
	if msg.lower().find('imdb.com/title/') != -1:
		imdb_id = msg.lower()[msg.lower().find('imdb.com/title/')+15:][:9]
		g.csend(chanq, commands.imdb_info('id', imdb_id))


def botendtriggerd(chant, usert, msgt):
	if not general.check_operator(usert):
		outp = 'You do not have permission to use any of these commands.'
	else:
		msgt = general.check_bottriggers(msgt).split()
		outp = commands.operator_commands(chant, msgt)
	if outp is not None:
		for line in outp.split('\n'):
			g.csend(chant, line)
			time.sleep(1)


def work_line(chanw, userw, msgw):
	msgw = general.check_midsentencecomment(msgw)
	msgw, rec, notice, pm = general.checkrec(chanw, userw, msgw)
	outp = commands.check_called(chanw, userw, msgw)
	if outp is not None:
		for line in outp.split('\n'):
			g.csend(chanw, line, notice, pm, rec)
			time.sleep(1)


if __name__ == '__main__':
	thread.start_new_thread(automatics.get_ftime, ())
	connect(config.server, config.port)
	thread.start_new_thread(automatics.autoping, ())
	thread.start_new_thread(automatics.autoweather, ())
	s = connection.s
	readbuffer = ''
	while True:
		readbuffer = readbuffer + s.recv(2048)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for rline in temp:
			rline = string.rstrip(rline)
			rline = string.split(rline)
			g = general
			if not server_responses(rline) and len(rline) > 3:
				msg = ' '.join(rline[3:])[1:]
				user = rline[0][1:][:rline[0].find('!')][:-1]
				chan = rline[2]
				if config.verbose:
					print g.ftime + ' << ' + ' '.join(rline)
				else:
					print g.ftime + ' << ' + chan + ' <{}> '.format(user) + msg
				if general.check_bottriggers(msg):
					thread.start_new_thread(botendtriggerd, (chan, user, msg),)
					break
				thread.start_new_thread(find_imdb_link, (chan, msg), )
				msg = general.check_midsentencetrigger(msg)
				msg = general.check_triggers(msg)
				if msg:
					thread.start_new_thread(work_line, (chan, user, msg), )