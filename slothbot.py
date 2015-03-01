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
if os.path.exists('config.py') == False:
	definitions.generate_config()	
import config
import variables

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
			print variables.ftime + ' >> ' + "PONG %s\r\n" % line[1]
			s.send("PONG %s\r\n" % line[1])
		if line[1] == 'MODE' and mode_found == False:
			mode_found = True
			s.send('JOIN %s\n' % config.channel)
		if config.verbose == True and mode_found == False:
			print variables.ftime + ' << ' + ' '.join(line)
		else:
			print variables.ftime + ' << ' + ' '.join(line[2:])

	## START OF NON-SYSTEM FUNCTIONS ##
		if mode_found == True:
			msg = ' '.join(line[3:])[1:]
			user = line[0][1:][:line[0].find('!')][:-1]
			definitions.add_defs(user, msg, line)
			if len(line) > 3:
				chan = line[2]
			else:
				chan = channel
	                if config.verbose == True and mode_found == False:
        	                print variables.ftime + ' << ' + ' '.join(line)
                	else:
                        	print variables.ftime + ' << ' + '%s <%s> %s' % (chan, user, msg)
			if msg.lower() == ':ping':
				csend('%s: PONG!' % user)
			if msg.lower() == '%s: update' % config.bot_nick.lower() and user == config.admin:
				definitions = reload(definitions)
				config = reload(config)
				csend('Updated.')
                        if msg.lower() == '%s: restart' % config.bot_nick.lower() and user == config.admin:
                                csend('Restarting..')
				args = ['','']
				ssend('QUIT :Restarting')
				os.execl(sys.argv[0], 'restart')
				csend('Done')
