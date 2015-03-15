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
import lists
import ceq
import json, urllib2

args = sys.argv
if os.path.exists('config.py') == False:
	print 'No configuration-file found.'
	definitions.generate_config()
	os.execl(args[0], '')
if os.path.exists('lists.py') == False:
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

print 'Connecting to ' + config.server + ' with port ' + str(config.port)
version = variables.version
s = soconnect.s
readbuffer = ''
s.connect((config.server, config.port))
s.send("PASS %s\n" % (config.password))
s.send("USER %s %s %s :%s\n" % (config.bot_username, config.bot_hostname, config.bot_servername, config.bot_realname))
s.send("NICK %s\n" % (config.bot_nick))

ssend = variables.ssend
csend = variables.csend
psend = variables.psend
end_names = False
mode_found = False
changed_nick = False
midsentence_trigger = False
midsentence_comment = True
dev = False
channel = config.channel

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
		if line[1] == '433' and mode_found == False:
			config.bot_nick = config.bot_nick2
			ssend('NICK %s' % config.bot_nick)
			if changed_nick:
				config.bot_nick = config.bot_nick + '_'
				ssend('NICK %s' % config.bot_nick)
				break
			break
		if line[1] == 'MODE' and mode_found == False:
			mode_found = True
			s.send('JOIN %s\n' % config.channel)
		if len(line) > 2:
			if line[1].lower() == 'part':
				if config.verbose == True:
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
			if midsentence_trigger:
				if msg.lower().find(" :(") != -1 and msg.lower().find(')') != -1:
					print msg
					msg = msg[msg.find(' :('):msg.find(')')].replace(' :(', ':')
					variables.msg = msg
					print msg
			if midsentence_comment:
				if msg.lower().find("\\") != -1:
					msg = variables.msg[:msg.find("\\")]
					print msg
					variables.msg = msg
			if len(line) > 2:
				if line[2].lower() == config.bot_nick.lower() and variables.check_operator():
					print 'Command from operator %s recieved: %s' % (user, msg)
					definitions.operator_commands(pm, msg)
				#	if len(msg.split()) > 1:
				#		if msg.split()[0].lower() == 'nick':
				#			config.bot_nick = msg.split()[1]
				#			print ' * Changed nick to ' + config.bot_nick
				#	ssend(msg)
				#	break
			if lists.ignorelist and lists.whitelist:
				print 'WARNING: Both whitelist and ignorelist is enabled in the config-file. Please change it so only one of them is True.'
				print "Until so, both the whitelist and the ignorelist will be ignored."
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



			if line[1] == '366' and end_names == False:
				end_names = True
				print "=======================================\n======= Successfully Connected ========\n======================================="
				print "Connected users on %s: %s\n" % (users_c, users_u)
			if msg.lower() == ':ping':
				csend('%s: PONG!' % user)
				break
			if msg.lower() == '%s: update' % config.bot_nick.lower() and variables.check_operator():
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
			if msg.lower() == '%s: restart' % config.bot_nick.lower() and variables.check_operator():
				csend('Restarting..')
				ssend('QUIT %s :Restarting' % config.channel)
				print args[0], 'channel', '"%s"' % config.channel
				if len(args) > 2:
					os.execl(args[0], '"%s"' % config.channel)
				else:
					os.execl(args[0], '')
				csend('Done')
				break
			if msg.lower() == '%s: quit' % config.bot_nick.lower() and variables.check_operator():
				csend(random.choice(variables.leave_messages))
				ssend('QUIT %s :%s' % (config.channel, config.leave_message))
				sys.exit()
			if ' '.join(msgs[:2]).lower() == '%s: join' % config.bot_nick.lower() and msgs[
				2] != '' and variables.check_operator():
				ssend('JOIN %s' % msgs[2])
				csend('Joined %s' % msgs[2])
			if ' '.join(msgs[:2]).lower() == '%s: part' % config.bot_nick.lower() and variables.check_operator():
				if len(msgs) > 2:
					chan_to_leave = msgs[2]
					ssend('PART %s :%s' % (chan_to_leave, config.leave_message))
					csend('Parted with %s.' % chan_to_leave)
				else:
					chan_to_leave = config.channel
					csend(random.choice(variables.leave_messages))
					ssend('PART %s :%s' % (chan_to_leave, config.leave_message))
			if msg.lower() == '%s: compile' % config.bot_nick.lower() and variables.check_operator():
				print 'Compiling..'
				try:
					os.system("python -O -m py_compile")#
					csend('Successfully compiled. Restarting..')
					ssend('QUIT ' + config.leave_message)
					if len(args) > 2:
						os.execl(args[0], '"%s"' % config.channel)
					else:
						os.execl(args[0], '')
				except:
					csend('Compilation failed.')
			if msg.lower() == '%s: git-update' % config.bot_nick.lower() and variables.check_operator():
				print 'Pulling from Git and updating...'
				try:
					url4 = "https://api.github.com/repos/johanhoiness/alison/commits"
					data4 = json.load(urllib2.urlopen(url4, timeout=4))
					csend(ceq.ccyan + 'Last commit: ' + ceq.corange + data4[0]['commit']['message'])
				except:
					print 'Failed to get commit-message from git.'
				try:
					os.system("git pull http://github.com/johanhoiness/alison")
#					print "OUTP: " + outp
#					comn = str(os.system("git log -n 6 | tail -1 | sed 's/\ \ \ \ //g'"))
#					print "COMN: " + comn
#					if str(outp).split("\n")[-1].lower() == "already up-to-date.":
#						csend("Already up to date.")
#						break
#					csend(str(outp).split("\n")[-1] + ", last comment: " + comn)
					csend('Successfully installed. Restarting..')
					ssend('QUIT ' + config.leave_message)
					if len(args) > 2:
						os.execl(args[0], '"%s"' % config.channel)
					else:
						os.execl(args[0], '')
				except:
					csend('Download or installation failed.')

			if dev:
				definitions.add_defs(user, msg, line)
			else:
				try:
					definitions.add_defs(user, msg, line)
				except:
					print 'Unknown error. (definitions.add_defs)'
					csend('Unknown error. (definitions.add_defs)')
#
