#!/usr/bin/python
import socket
import sys
import os
import random
import time
import os.path
from datetime import datetime
import definitions
if os.path.exists('config.py') == False:
	definitions.generate_config()	
import config
import variables

version = variables.version

## CONNECTION ##
#print "Connecting to " + config.server
variables.irc.connect((config.server, config.port))
variables.irc.send("PASS %s\n" % (config.password))
variables.irc.send("USER %s %s %s :%s\n" % (config.bot_username, config.bot_hostname, config.bot_servername, config.bot_realname))
variables.irc.send("NICK %s\n" % (config.bot_nick))

hostname_found = False
mode_found = False
send_chan = definitions.send_chan
channel = config.channel
while 1:
	## ESSENSIAL FOR SYSTEM ##
	ftime = variables.ftime
	variables.raw_text = variables.irc.recv(2040)
	raw_text = variables.raw_text
	variables.msg = raw_text[raw_text.find(':'):500][1:500]
	variables.msg = variables.msg[variables.msg.find(':'):500][1:500].replace('\n', '').replace('\r', '')
	variables.user = raw_text[1:raw_text.find('!')]
	user = variables.user
	msg = variables.msg
	if user != "" and mode_found == True:
		print ftime + user + ": " + msg
	else:
		print ftime + raw_text
	if config.verbose == True:
		print ftime + raw_text
	if raw_text.find('PING') != -1:
		variables.irc.send('PONG ' + raw_text[raw_text.find(":"):] + '\r\n')
		print ftime + ' --> ' + 'PONG ' + raw_text[raw_text.find(":"):] + '\r\n'
	if raw_text.find('/QOUTE PASS') != -1:
		variables.irc.send('PONG %s' % (raw_test[raw_text.find('/QUOTE PASS '):][12:][:raw_text.find(' ')]))
		print ftime + ' --> ' + 'PONG %s' % (raw_test[raw_text.find('/QUOTE PASS '):][12:][:raw_text.find(' ')])
	if raw_text.find('MODE') != -1 and mode_found == False:
		mode_found = True
		variables.irc.send("PRIVMSG nickserv :identify %s %s\r\n" % (config.bot_username, config.password))
		variables.irc.send("JOIN %s\n" % (channel))

	## START OF NON-ESSENSIAL FOR SYSTEM ##
	if msg.lower().find("%s: leave" % (config.bot_nick.lower())) != -1 and user == config.admin:
		send_chan(random.choice(variables.leave_messages))
		variables.irc.send("QUIT :%s\n" % (config.leave_message))
		sys.exit("Bot recieved leave-command.")
	if msg.lower().find(":ping") != -1:
		definitions.send_chan("%s: PONG!" % (user))
	if msg.lower() == ":version":
		send_chan("Running %s version %s" % (config.bot_nick, version))
	if msg.lower() == ":help":
		definitions.helpx()
