#!/usr/bin/python
import socket
import sys
import os
import random
import time
import string
import os.path
from multiprocessing import Process
from datetime import datetime
import definitions
args = sys.argv
if os.path.exists('config.py') == False:
	print 'No configuration-file found.'
	definitions.generate_config()
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
s = variables.s
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
channel = config.channel
while 1:
	readbuffer = readbuffer+variables.s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop( )

	for line in temp:
		line = string.rstrip(line)
		line = string.split(line)
		if(line[0] == "PING"):
			if config.verbose == True:
				print variables.ftime + ' >> ' + "PONG %s\r\n" % line[1]
			s.send("PONG %s\r\n" % line[1])
                if line[1] == '433' and mode_found == False:
                        config.bot_nick = config.bot_nick2
                        ssend('NICK %s' % config.bot_nick)
		if line[1] == 'MODE' and mode_found == False:
			mode_found = True
			s.send('JOIN %s\n' % config.channel)
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
			definitions.add_defs(user, msg, line)
			variables.ftime = "[%s:%s:%s]" % (datetime.now().hour, datetime.now().minute, datetime.now().second)
			msgs = msg.split()
			if len(line) > 3:
				chan = line[2]
			else:
				chan = channel
	                if config.verbose == True and mode_found == False:
        	                print variables.ftime + ' << ' + ' '.join(line)
                	elif config.verbose == True:
				print variables.ftime + ' << ' + ' '.join(line)
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
			if msg.lower() == '%s: update' % config.bot_nick.lower() and user == config.admin:
				definitions = reload(definitions)
				config = reload(config)
				csend('Updated.')
                        if msg.lower() == '%s: restart' % config.bot_nick.lower() and user == config.admin:
                                csend('Restarting..')
				ssend('QUIT :Restarting')
				os.execl(args[0], '')
				csend('Done')
                        if msg.lower() == '%s: leave' % config.bot_nick.lower() and user == config.admin:
                                csend(random.choice(variables.leave_messages))
                                ssend('QUIT %s' % config.leave_message)
				sys.exit()
			if ' '.join(msgs[:2]).lower() == '%s: join' % config.bot_nick.lower() and msgs[2] != '' and user == config.admin:
				ssend('JOIN %s' % msgs[2])
				csend('Joined %s' % msgs[2])
			if ' '.join(msgs[:2]).lower() == '%s: part' % config.bot_nick.lower() and user == config.admin:
				if len(msgs) > 2:
                                        chan_to_leave = msgs[2]
                                        ssend('PART %s' % chan_to_leave)
                                        csend('Parted with %s.' % chan_to_leave)
				else:
					chan_to_leave = config.channel
					csend(random.choice(variables.leave_messages))
					ssend('PART %s' % chan_to_leave)
