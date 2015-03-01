#!/usr/pyton
import time
import socket
import sys
import os
import uuid
import string
from datetime import datetime
def random_string(string_length=10):
       random = str(uuid.uuid4())
       random = random.upper()
       random = random.replace("-","")
       return random[0:string_length]
def generate_config():
	c_server = raw_input('Server you want to connect to: ')
        while c_server == '':
                c_server = raw_input('You didnt type anything when I asked for what server to connect to. Say it now: ')
        c_port = raw_input('Connect using port[6667]: ')
        c_channel = raw_input('Channel you want to connect to: ')
        while c_channel == '':
                c_channel = raw_input('You didnt type anything when I asked for what channel to connect to. Say it now: ')
        c_nick = raw_input('The nickname of the bot: ')
        while c_nick == '':
                c_nick = raw_input('You didnt type anything when I asked what nicname the bot should have. Say it now: ')
	c_nick2 = raw_input('The second nickname of the bot, incase first is taken[%s2]: ' % c_nick)
        c_username = raw_input('The username of the bot[same as nick]: ')
        c_hostname = raw_input('The hostname of the bot[same as nick]: ')
        c_servername = raw_input('The servername of the bot[same as nick]: ')
        c_realname = raw_input('The realname of the bot[Bot created by Johan H. in Python]: ')
        c_password = raw_input('The password of the username(This is if you want to connect it to a registered user)[]: ')
        c_admin = raw_input('The admin of the bot: ')
        while c_admin == '':
                c_admin = raw_input('You didnt type anything when I asked what username is to be the admin. Say it now: ')
        c_leave_message = raw_input('Leave message(might not work)[Cya]: ')
        c_verbose = raw_input('Do you want to enable verbose, thus seeing all messages from and to the server?(y/n)[n]: ')
	if c_port == '':
		c_port = 6667
	if c_nick2 == '':
		c_nick2 = c_nick + '2'
        if c_username == '':
                c_username = c_nick
        if c_password == '':
                c_password = random_string()
        if c_hostname == '':
                c_hostname = c_nick
        if c_servername == '':
                c_servername = c_nick
        if c_realname == '':
                c_realname = 'Bot created by Johan H. in Python'
        if c_leave_message == '':
                c_leave_message = 'Cya'
        if c_verbose == '' or c_verbose.lower() == 'n':
                c_verbose = 'False'
	elif c_verbose.lower() == 'y':
		c_verbose = 'True'
	f = open('config.py', 'w')
	f.write('server = "%s"\n' % (c_server))
        f.write('port = %d\n' % (c_port))
        f.write('channel = "%s"\n' % (c_channel))
        f.write('bot_nick = "%s"\n' % (c_nick))
	f.write('bot_nick2 = "%s"\n' % (c_nick2))
        f.write('bot_username = "%s"\n' % (c_username))
        f.write('bot_hostname = "%s"\n' % (c_hostname))
        f.write('bot_servername = "%s"\n' % (c_servername))
        f.write('bot_realname = "%s"\n' % (c_realname))
        f.write('password = "%s"\n' % (c_password))
        f.write('admin = "%s"\n' % (c_admin))
        f.write('leave_message = "%s"\n' % (c_leave_message))
        f.write('verbose = %s\n' % (c_verbose))
	f.close()
	print 'Done. The configuration-file has been made and is placed in the same folder as the main program, labeled "config.py".'
	print 'If you want to edit any settings, edit the config-file manually, or delete the config-file to reset.'
if os.path.exists('config.py') == True:
	import config
	import definitions
	import variables
	from urllib2 import urlopen
	
	ssend = variables.ssend
	csend = variables.csend
	psend = variables.psend
	def imdb_info(imdb_id):
		csend(imdb_id)
		imdb_api = urlopen('http://www.omdbapi.com/?i=%s&plot=short&r=json' % imdb_id)
		print imdb_api
	def add_defs(user, msg, line):
		words = msg.split( )
		if len(words) > 0:
			if words[0].lower() == ':test':
				csend('%s: Running.' % variables.ftime)
			if msg.lower() == ':version':
				csend('Running %s v%s' % (config.bot_nick, variables.version))
			if words[0] == ':say':
				csend(' '.join(words[1:]))
			if msg.find('imdb.com/title') != -1:
				csend('IMDB-link found.')
				imdb_id = msg[msg.find('imdb.com/title/'):][15:24]
				imdb_info(imdb_id)				
			if msg.find('johan') != -1:
				psend('Sloth', msg)
