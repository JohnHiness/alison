#!/usr/bin/python

import sys
import os
import random
import time
import string
import os.path
import definitions
import soconnect
from time import strftime
import revar
import ceq
import json, urllib2
import thread


args = sys.argv

if os.path.exists('config.py') == False:
	print 'No configuration-file found.'
	definitions.generate_config()
	os.execl(args[0], '')
if os.path.exists('revar.py') == False:
	print 'No whitelist/ignorelist-file found.'
	print 'Generating files'
	definitions.generate_lists()
	os.execl(args[0], '')
import config
import variables

variables.args = args


if __name__ == "__main__":
	if len(sys.argv) > 1:
		if args[1].lower() == 'channel' and len(args) > 2:
			config.channel = args[2]
			print 'Channel set to %s' % args[2]
		elif args[1].lower() == 'reconfig' or args[1].lower() == 'reconfigure':
			print 'Reconfiguring configuartions. All previous configurations will be replaced.'
			definitions.generate_config()
			sys.exit('Configurations done.')
		elif args[1].lower() == 'help':
			print "Syntax: python %s <channel channelname | help | reconfigure>" % (args[0])
			sys.exit()
		elif args[1].lower() == 'verbose':
			config.verbose = True
			print 'Verbose is set to %s' % config.verbose
		else:
			print "Syntax: python %s <channel channelname | help | reconfigure>" % (args[0])
			sys.exit()
	if revar.bot_nick == '':
		revar.bot_nick = config.bot_nick
	if revar.operators == [] or revar.operators == '':
		revar.operators = config.operator.replace(', ', ',').replace(' ', '').split(',')
	if revar.channels == '' or revar.channels == []:
		revar.channels == config.channel.replace(', ', ',').replace(' ', ',').split(',')




def autoweather():
	while True:
		if revar.autoweather and time.time() - variables.last_time > 90 and int(strftime('%H%M')) == revar.autoweather_time:
			variables.last_time = time.time()
			outp = ''
			outp = definitions.weather(revar.location, True)
			if outp != '':
				variables.ssend("PRIVMSG {0} :".format(','.join(revar.channels)) + outp)
		time.sleep(1)


def autoping():
	while True:
		if time.time() - variables.autoping > 60:
			variables.ssend('PING DoNotTimeoutMePlz')
			variables.autoping = time.time()

global end_names
global mode_found
global muted
global changed_nick
global users_c
global users_u
end_names = False
mode_found = False
muted = False
changed_nick = False

def workline(line):
	try:
		line = string.rstrip(line)
		line = string.split(line)
		if ' '.join(line).find('\x0f') != -1:
			print 'Breakcode found: ' + ' '.join(line)
			return

		global end_names, users_c, users_u
		global mode_found
		global muted
		global changed_nick


		variables.ftime = '[' + strftime('%H:%M:%S') + ']'

		if len(line) > 1 and line[1].lower() == 'pong':
			variables.ssend("TIME")
			variables.ssend("WHOIS " + revar.bot_nick.lower())

		if line[0] == "PING":
			if config.verbose:
				print variables.ftime + ' >> ' + "PONG %s" % line[1]

			s.send("PONG %s\r\n" % line[1])
			variables.ssend("TIME")
			variables.ssend("WHOIS " + revar.bot_nick.lower())

		if len(line) > 3 and line[3].lower() == ":\x01ping" and (line[1].lower() == 'notice' or line[1].lower() == 'privmsg'):
			if len(line) > 4:
				variables.ssend("PRIVMSG {0} :\x01PONG {1}".format(line[0][1:' '.join(line).find("!")], ' '.join(line[4:])))

			else:
				variables.ssend("PRIVMSG {0} :\x01PONG\x01".format(line[0][1:' '.join(line).find("!")]))

			return

		if len(line) > 3 and line[3].lower() == ":\x01version\x01" and (line[1].lower() == 'notice' or line[1].lower() == 'privmsg'):
			variables.ssend("PRIVMSG {0} :\x01Running the IRC Bot Alison version, {1}\x01".format(line[0][1:' '.join(line).find("!")], variables.version))
			return

		if line[1] == '433' and mode_found == False:
			revar.bot_nick = config.bot_nick2
			ssend('NICK %s' % revar.bot_nick)
			if changed_nick:
				revar.bot_nick = revar.bot_nick + '_'
				ssend('NICK %s' % revar.bot_nick)
				return

			changed_nick = True
			return

		if len(line) > 2 and line[1] == '391':
			revar.bot_nick = line[2]

		if len(line) > 2 and line[1].lower() == 'join':
			if not line[2].lower() in revar.channels:
				revar.channels.append(line[2].lower())

		if len(line) > 2 and line[1].lower() == 'part':
			if line[2].lower() in revar.channels:
				try:
					revar.channels.append(line[2].lower())

				except:
					pass

		if len(line) > 3 and line[1] == '319' and line[2].lower() == revar.bot_nick.lower():
			revar.channels = ' '.join(line[4:])[1:].replace('+', '').replace('@', '').lower().split()

		if len(line) > 2:
			if line[1].lower() == 'part':
				if config.verbose == True:
					print variables.ftime + ' << ' + ' '.join(line)

				else:
					print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(line[0][1:][:line[0].find('!')][:-1], line[2]) + ' '.join(line[3:])[1:]

				time.sleep(0.5)
				variables.ssend("WHOIS " + revar.bot_nick.lower())
				return

			if line[1].lower() == "quit":
				if config.verbose:
					print variables.ftime + ' << ' + ' '.join(line)

				else:
					print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(line[0][1:][:line[0].find('!')][:-1], line[2]) + ' '.join(line[3:])[1:]

				return

			if line[1].lower() == "quit":
				if config.verbose == True:
					print variables.ftime + ' << ' + ' '.join(line)

				else:
					print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(line[0][1:][:line[0].find('!')][:-1], line[2]) + ' '.join(line[3:])[1:]

				return

		if config.verbose == True and mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line).encode('utf-8')

		elif mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line[2:]).encode('utf-8')

		## START OF NON-SYSTEM FUNCTIONS ##
		if len(line) > 3:
			config.channel = line[2]

		if len(line) > 3:
			chan = line[2]
		else:
			chan = channel
		msg = ' '.join(line[3:])[1:]
		user = line[0][1:][:line[0].find('!')][:-1]
		variables.user = user
		msgs = msg.split()
		variables.msg = msg
		variables.msgs = msgs
		variables.line = line

		if len(msgs) > 1 and (msgs[0].lower() == revar.bot_nick.lower() or (msgs[0][:-1].lower() == revar.bot_nick.lower() and msgs[0][-1] in revar.end_triggers) ) and variables.check_operator():
			if msgs[1].lower() == 'mute' and not muted:
				muted = True
				return

			if msgs[1].lower() == 'umute' or msgs[1].lower() == 'unmute':
				muted = False

		if muted:
			print 'Muted: ' + ' '.join(line)
			return

		if revar.midsentence_trigger:
			if msg.lower().find(" :(") != -1 and msg.lower().find(')') != -1:
				print msg
				msg = msg[msg.find(' :('):msg.find(')')].replace(' :(', ':')
				variables.msg = msg
				print msg

		if revar.midsentence_comment:
			if msg.lower().find("\\") != -1:
				msg = variables.msg[:msg.find("\\")]
				print msg
				variables.msg = msg

		if len(line) > 2:
			if line[2].lower() == revar.bot_nick.lower() and variables.check_operator():
				print 'Command from operator %s recieved: %s' % (user, msg)
				ssend(msg)

		if revar.ignorelist_set and revar.whitelist_set:
			print 'WARNING: Both whitelist and ignorelist is enabled in the config-file. Please change it so only one of them is True.'
			# print "Until so, both the whitelist and the ignorelist will be ignored."

		else:
			try:
				if variables.check_whitelist():
					print 'Ignored user %s.' % user
					return

			except:
				csend(chan, 'Error checking whitelist.')

			try:
				if variables.check_ignorelist():
					print 'Ignoring user %s.' % user
					return

			except:
				csend(chan, 'Error checking ignorelist.')

		if revar.outputredir:
			try:
				definitions.checkrec(msgs)
				msg = variables.msg
				msgs = variables.msgs
				line = variables.line

			except:
				csend(chan, 'Unknown error: definitions.checkrec(msgs)')


		if config.verbose == True and mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line).replace('\n', '').encode('utf-8')

		elif config.verbose == True:
			print variables.ftime + ' << ' + ' '.join(line).replace('\n', '')

		elif config.verbose == False and (line[0] != 'PING'\
				and (len(line) > 1 and line[1] != '391')\
				and (len(line) > 1 and line[1] != '311')\
				and (len(line) > 1 and line[1] != '319')\
				and (len(line) > 1 and line[1] != '312')\
				and (len(line) > 1 and line[1] != '317')\
				and (len(line) > 1 and line[1] != '330')\
				and (len(line) > 1 and line[1] != '318')):
			print variables.ftime + (' << ' + '%s <%s> %s' % (chan, user, msg)).encode('utf-8')

		if line[1] == '353':
			users_c = line[4]
			users_u = ', '.join(line[5:])[1:]
			if end_names:
				print "Connected users on %s: %s" % (users_c, users_u)

		if line[1] == '432':
			ssend("PRIVMSG {0} :Erroneus nickname.".format(variables.nick_last_channel))

		if line[1] == '433':
			ssend("PRIVMSG {0} :Nickname is allready in use.".format(variables.nick_last_channel))

		if line[1] == 'NICK':
			ssend('TIME')

		if line[1] == '366' and not end_names:
			end_names = True
			print "\n=======================================\n======= Successfully Connected ========\n=======================================\n"
			print "Connected users on %s: %s\n" % (users_c, users_u)

		if msg.lower() == '%s: restart' % revar.bot_nick.lower() and variables.check_operator():
			csend(chan, 'Restarting..')
			ssend('QUIT %s :Restarting' % chan)
			print args[0], 'channel', '"%s"' % chan
			python = sys.executable
			print str(python)+'||'+str(python)+'||'+ str(* sys.argv)
			os.execl(python, python, * sys.argv)
			csend(chan, 'Done')
			return

		if msg.lower() == '%s: quit' % revar.bot_nick.lower() and variables.check_operator():
			csend(chan, random.choice(variables.leave_messages))
			ssend('QUIT %s :%s' % (chan, config.leave_message))
			sys.exit()

		if ' '.join(msgs[:2]).lower() == '%s: join' % revar.bot_nick.lower() and msgs[
			2] != '' and variables.check_operator():
			ssend('JOIN %s' % msgs[2])
			csend(chan, 'Joined %s' % msgs[2])

		if ' '.join(msgs[:2]).lower() == '%s: part' % revar.bot_nick.lower() and variables.check_operator():
			if len(msgs) > 2:
				chan_to_leave = msgs[2]
				ssend('PART %s :%s' % (chan_to_leave, config.leave_message))
				csend(chan, 'Parted with %s.' % chan_to_leave)

			else:
				chan_to_leave = chan
				csend(chan, random.choice(variables.leave_messages))
				ssend('PART %s :%s' % (chan_to_leave, config.leave_message))

		if msg.lower() == '%s: compile' % revar.bot_nick.lower() and variables.check_operator():
			print 'Compiling..'
			try:
				outputt = os.system("python -O -m py_compile alison.py definitions.py variables.py config.py ceq.py revar.py soconnect.py")
				if outputt != 0:
					csend(chan, 'Compilation failed.')
					return

				csend(chan, 'Successfully compiled. Restarting..')
				ssend('QUIT ' + config.leave_message)
				if len(args) > 2:
					os.execl(args[0], '"%s"' % chan)

				else:
					os.execl(args[0], '')

			except:
				csend(chan, 'Compilation failed.')


		try:
			definitions.add_defs(chan, user, msg, line)

		except BaseException, exc:
			if revar.dev:
				print 'Error in alison.py, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, 'Error in alison.py, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))

			else:
				csend(chan, "Something went wrong.")
	except BaseException, exc:
		if revar.dev:
			print 'Error in alison.workline(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
			csend(chan, 'Error in alison.workline(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
		else:
			csend(chan, "Something went wrong.")


if __name__ == "__main__":
	print 'Connecting to ' + config.server + ' with port ' + str(config.port)
	version = variables.version
	s = soconnect.s
	readbuffer = ''
	try:
		s.connect((config.server, config.port))
	except:
		print 'Failed to connect.'
		sys.exit(1)
	s.send("PASS %s\n" % (config.password))
	s.send("USER %s %s %s :%s\n" % (config.bot_username, config.bot_hostname, config.bot_servername, config.bot_realname))
	s.send("NICK %s\n" % (revar.bot_nick))
	ssend = variables.ssend
	csend = variables.csend
	psend = variables.psend
	channel = ','.join(revar.channels)

	autoweather_on = False
	autoping_on = False

	while 1:
		readbuffer = readbuffer + variables.s.recv(2048)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()

		for rline in temp:
			rawline = rline
			if not mode_found:
				rline = string.rstrip(rline)
				rline = string.split(rline)
				variables.ftime = '[' + strftime('%H:%M:%S') + ']'
				if rline[0] == "PING":
					if config.verbose:
						print variables.ftime + ' >> ' + "PONG %s" % rline[1]
					s.send("PONG %s\r\n" % rline[1])
				if rline[1] == '433':
					if not changed_nick:
						revar.bot_nick = config.bot_nick2
						ssend('NICK %s' % revar.bot_nick)
					if changed_nick:
						revar.bot_nick = revar.bot_nick + '_'
						ssend('NICK %s' % revar.bot_nick)
					changed_nick = True
					break
				if rline[1] == 'MODE' and mode_found == False:
					mode_found = True
					variables.ssend('JOIN %s' % ','.join(revar.channels))
					if not autoweather_on:
						autoweather_on = True
						thread.start_new_thread(autoweather, ())
					if not autoping_on:
						autoping_on = True
						thread.start_new_thread(autoping, ())
				if len(rline) > 3 and rline[1] == '319' and rline[2].lower() == revar.bot_nick.lower():
					revar.channels = ' '.join(rline[4:])[1:].replace('+', '').replace('@', '').lower().split()
				if len(rline) > 2:
					if rline[1].lower() == 'part':
						if config.verbose == True:
							print variables.ftime + ' << ' + ' '.join(rline)
						else:
							print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(rline[0][1:][:rline[0].find('!')][:-1], rline[2]) + ' '.join(rline[3:])[1:]
						variables.ssend("WHOIS " + revar.bot_nick.lower())
						break
					if rline[1].lower() == "quit":
						if config.verbose:
							print variables.ftime + ' << ' + ' '.join(rline)
						else:
							print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(rline[0][1:][:rline[0].find('!')][:-1], rline[2]) + ' '.join(rline[3:])[1:]
						break
					if rline[1].lower() == "quit":
						if config.verbose == True:
							print variables.ftime + ' << ' + ' '.join(rline)
						else:
							print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(rline[0][1:][:rline[0].find('!')][:-1], rline[2]) + ' '.join(rline[3:])[1:]
						break
				if config.verbose == True and mode_found == False:
					print variables.ftime + ' << ' + ' '.join(rline).encode('utf-8')
				elif mode_found == False:
					print variables.ftime + ' << ' + ' '.join(rline[2:]).encode('utf-8')

			if mode_found and rawline.split()[0].find('!') == -1:
				workline(rawline)
			elif mode_found:
				thread.start_new_thread(workline, (rawline,))
