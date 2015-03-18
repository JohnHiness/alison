#!/usr/bin/python
import socket
import sys
import os
import random
import time
import string
import os.path
from multiprocessing import Process
import datetime
import definitions
import soconnect
from time import strftime
import revar
import ceq
import json, urllib2

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
end_names = False
mode_found = False
muted = False
changed_nick = False
midsentence_trigger = False
channel = ','.join(revar.channels)

while 1:
	readbuffer = readbuffer + variables.s.recv(2048)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		if ' '.join(line).find('\x0f') != -1:
			print 'Breakcode found.'
			break
		line = string.rstrip(line)
		line = string.split(line)
		variables.ftime = '[' + strftime('%H:%M:%S') + ']'
		if line[0] == "PING":
			if config.verbose:
				print variables.ftime + ' >> ' + "PONG %s" % line[1]
			s.send("PONG %s\r\n" % line[1])
			variables.ssend("TIME")
			variables.ssend("WHOIS " + revar.bot_nick.lower())
		if line[1] == '433' and mode_found == False:
			revar.bot_nick = config.bot_nick2
			ssend('NICK %s' % revar.bot_nick)
			if changed_nick:
				revar.bot_nick = revar.bot_nick + '_'
				ssend('NICK %s' % revar.bot_nick)
				break
			changed_nick = True
			break
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
		if line[1] == 'MODE' and mode_found == False:
			mode_found = True
			variables.ssend('JOIN %s' % ','.join(revar.channels))
			time.sleep(0.5)
			variables.ssend("WHOIS " + revar.bot_nick.lower())
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
				break
			if line[1].lower() == "quit":
				if config.verbose:
					print variables.ftime + ' << ' + ' '.join(line)
				else:
					print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(line[0][1:][:line[0].find('!')][:-1], line[2]) + ' '.join(line[3:])[1:]
				break
			if line[1].lower() == "quit":
				if config.verbose == True:
					print variables.ftime + ' << ' + ' '.join(line)
				else:
					print variables.ftime + " << " + "{0:s} has left {1:s}; ".format(line[0][1:][:line[0].find('!')][:-1], line[2]) + ' '.join(line[3:])[1:]
				break
		if config.verbose == True and mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line)
		elif mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line[2:])

		## START OF NON-SYSTEM FUNCTIONS ##
		if mode_found == True:
			if len(line) > 3:
				config.channel = line[2]
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
					break
				if (msgs[1].lower() == 'umute' or msgs[1].lower() == 'unmute'):
					muted = False
			if muted:
				print 'Muted: ' + ' '.join(line)
				break
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
				#	if len(msg.split()) > 1:
				#		if msg.split()[0].lower() == 'nick':
				#			revar.bot_nick = msg.split()[1]
				#			print ' * Changed nick to ' + revar.bot_nick
				#	ssend(msg)
				#	break
			if revar.ignorelist_set and revar.whitelist_set:
				print 'WARNING: Both whitelist and ignorelist is enabled in the config-file. Please change it so only one of them is True.'
				#print "Until so, both the whitelist and the ignorelist will be ignored."
			else:
				try:
					if variables.check_whitelist():
						print 'Ignored user %s.' % user
						break
				except:
					csend('Error checking whitelist.')
				try:
					if variables.check_ignorelist():
						print 'Ignoring user %s.' % user
						break
				except:
					csend('Error checking ignorelist.')
			if revar.outputredir:
				try:
					definitions.checkrec(msgs)
					msg = variables.msg
					msgs = variables.msgs
					line = variables.line
				except:
					csend('Unknown error: definitions.checkrec(msgs)')
			if len(line) > 3:
				chan = line[2]
			else:
				chan = channel
			if config.verbose == True and mode_found == False:
				print variables.ftime + ' << ' + ' '.join(line).replace('\n', '')
			elif config.verbose == True:
				print variables.ftime + ' << ' + ' '.join(line).replace('\n', '')
			elif config.verbose == False and line[0] != 'PING':
				print variables.ftime + ' << ' + '%s <%s> %s' % (chan, user, msg)
			if line[1] == '353':
				users_c = line[4]
				users_u = ', '.join(line[5:])[1:]
				if end_names == True:
					print "Connected users on %s: %s" % (users_c, users_u)
			if line[1] == '432':
				ssend("PRIVMSG {0} :Erroneus nickname.".format(variables.nick_last_channel))
			if line[1] == '433':
				ssend("PRIVMSG {0} :Nickname is allready in use.".format(variables.nick_last_channel))
			if line[1] == 'NICK':
				ssend('TIME')



			if line[1] == '366' and end_names == False:
				end_names = True
				print "=======================================\n======= Successfully Connected ========\n======================================="
				print "Connected users on %s: %s\n" % (users_c, users_u)
			if msg.lower() == ':ping':
				csend('%s: PONG!' % user)
				break
			if msg.lower() == '%s: update' % revar.bot_nick.lower() and variables.check_operator():
				print 'Updating...'
				chan = config.channel
				try:
					definitions = reload(definitions)
					config = reload(config)
					variables = reload(variables)
					lists = reload(lists)
					time.sleep(1)
					config.channel = chan
					csend('Updated successfully.')
				except:
					print 'Update error.'
					config.channel = chan
					csend('Update failed.')
				break
			if msg.lower() == '%s: restart' % revar.bot_nick.lower() and variables.check_operator():
				csend('Restarting..')
				ssend('QUIT %s :Restarting' % config.channel)
				print args[0], 'channel', '"%s"' % config.channel
				if len(args) > 2:
					os.execl(args[0], '"%s"' % config.channel)
				else:
					os.execl(args[0], '')
				csend('Done')
				break
			if msg.lower() == '%s: quit' % revar.bot_nick.lower() and variables.check_operator():
				csend(random.choice(variables.leave_messages))
				ssend('QUIT %s :%s' % (config.channel, config.leave_message))
				sys.exit()
			if ' '.join(msgs[:2]).lower() == '%s: join' % revar.bot_nick.lower() and msgs[
				2] != '' and variables.check_operator():
				ssend('JOIN %s' % msgs[2])
				csend('Joined %s' % msgs[2])
			if ' '.join(msgs[:2]).lower() == '%s: part' % revar.bot_nick.lower() and variables.check_operator():
				if len(msgs) > 2:
					chan_to_leave = msgs[2]
					ssend('PART %s :%s' % (chan_to_leave, config.leave_message))
					csend('Parted with %s.' % chan_to_leave)
				else:
					chan_to_leave = config.channel
					csend(random.choice(variables.leave_messages))
					ssend('PART %s :%s' % (chan_to_leave, config.leave_message))
			if msg.lower() == '%s: compile' % revar.bot_nick.lower() and variables.check_operator():
				print 'Compiling..'
				try:
					outputt = os.system("python -O -m py_compile alison.py definitions.py variables.py config.py ceq.py revar.py")
					if outputt != 0:
						csend('Compilation failed.')
						break
					csend('Successfully compiled. Restarting..')
					ssend('QUIT ' + config.leave_message)
					if len(args) > 2:
						os.execl(args[0], '"%s"' % config.channel)
					else:
						os.execl(args[0], '')
				except:
					csend('Compilation failed.')
			if msg.lower() == '%s: git-update' % revar.bot_nick.lower() and variables.check_operator():
				print 'Pulling from Git and updating...'
				try:
					url4 = "https://api.github.com/repos/johanhoiness/alison/commits"
					data4 = json.load(urllib2.urlopen(url4, timeout=4))
					csend(ceq.ccyan + 'Last commit: ' + ceq.cviolet + data4[0]['commit']['message'])
				except:
					print 'Failed to get commit-message from git.'
				try:
					outp = os.system("git pull http://github.com/johanhoiness/alison")
					if outp != 0:
						csend("Update failed.")
						break
					outp2 = os.system("python -O -m py_compile alison.py definitions.py variables.py config.py ceq.py revar.py soconnect.py")
					if outp2 != 0:
						csend("Download was successful but the compilation failed.")
						break
					csend('Successfully installed. Restarting..')
					ssend('QUIT ' + config.leave_message)
					if len(args) > 2:
						os.execl(args[0], '"%s"' % config.channel)
					else:
						os.execl(args[0], '')
				except:
					csend('Download or installation failed.')

			if revar.dev:
				definitions.add_defs(user, msg, line)
			else:
				try:
					definitions.add_defs(user, msg, line)
				except:
					print 'Unknown error. (definitions.add_defs)'
					csend('Unknown error. (definitions.add_defs)')
#
