__author__ = 'Johan Hoiness'

import uuid
import sys


def random_string(string_length=10):
	randomz = str(uuid.uuid4())
	randomz = randomz.upper()
	randomz = randomz.replace("-", "")
	return randomz[0:string_length]


def gen_config():
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
	c_operator = raw_input('The operator of the bot(You can have multiple operators. Just sperate the names with ,): ')
	while c_operator == '':
		c_operator = raw_input(
			'You didnt type anything when I asked what username is to be the operator(s). Say it now: ')
	c_leave_message = raw_input('Leave message(might not work)[Cya]: ')
	c_ignorelist = raw_input('Do you want to enable the ignore-list?\nYou can add users to be ignored in the revar.py -file that will be generated after this.(y/n)[n]: ')
	c_whitelist = raw_input('Do you want to enable the whitelist?\nYou can add users to only be listened to in the revar.py -file that will be generated after this.(y/n)[n]: ')
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
	if c_ignorelist == '' or c_verbose.lower() == 'n':
		c_ignorelist = 'False'
	elif c_ignorelist.lower() == 'y':
		c_ignorelist = 'True'
	else:
		c_ignorelist = 'False'
	if c_whitelist == '' or c_verbose.lower() == 'n':
		c_whitelist = 'False'
	elif c_whitelist.lower() == 'y':
		c_whitelist = 'True'
	else:
		c_whitelist = 'False'
	if c_verbose == '' or c_verbose.lower() == 'n':
		c_verbose = 'False'
	elif c_verbose.lower() == 'y':
		c_verbose = 'True'
	else:
		c_verbose = 'False'
	f = open('config.py', 'w')
	f.write('server = "%s"\n' % (c_server))
	f.write('port = %s\n' % (str(c_port)))
	f.write('channel = "%s"\n' % (c_channel))
	f.write('bot_nick = "%s"\n' % (c_nick))
	f.write('bot_nick2 = "%s"\n' % (c_nick2))
	f.write('bot_username = "%s"\n' % (c_username))
	f.write('bot_hostname = "%s"\n' % (c_hostname))
	f.write('bot_servername = "%s"\n' % (c_servername))
	f.write('bot_realname = "%s"\n' % (c_realname))
	f.write('password = "%s"\n' % (c_password))
	f.write('operator = "%s"\n' % (c_operator))
	f.write('leave_message = "%s"\n' % (c_leave_message))
	f.write('ignorelist = "%s"\n' % (c_ignorelist))
	f.write('whitelist = "%s"\n' % (c_whitelist))
	f.write('verbose = %s\n' % (c_verbose))
	f.close()
	print 'Done. The configuration-file has been made and is placed in the same folder as the main program, labeled "config.py".'
	print 'If you want to edit any settings, edit the config-file manually, or delete the config-file to reset.'

def gen_revar():
	try:
		import config
		channels = config.channel.replace(', ', ',').replace(' ', ',').split(',')
		ops = config.operator.replace(', ', ',').replace(' ', ',').split(',')
		f = open('revar.py', 'w')
		f.write("channels = " + str(channels)+'\n')
		f.write("bot_nick = \"%s\"" % (config.bot_nick) +'\n')
		f.write("triggers = [':']"+'\n')
		f.write("autoweather_time = 0900"+'\n')
		f.write("whitelist = []"+'\n')
		f.write("dev = True"+'\n')
		f.write("location = \"oslo\""+'\n')
		f.write("outputredir = True"+'\n')
		f.write("get_hash = True"+'\n')
		f.write("ignorelist = []"+'\n')
		f.write("autoweather = True"+'\n')
		f.write("ignorelist_set = False"+'\n')
		f.write("weather_custom = False"+'\n')
		f.write("end_triggers = [' ', '', ',', ':', '|']"+'\n')
		f.write("whitelist_set = False"+'\n')
		f.write("midsentence_comment = True"+'\n')
		f.write("midsentence_trigger = False"+'\n')
		f.write("operators = " + str(ops)+'\n')
		f.write("outputredir_all = False"+'\n')
		f.write("chatbotid = 71367"+'\n')
		f.write("deer_god = True"+'\n')
		f.close()
		print "Revar.py default configurations set and written."
	except BaseException as exc:
		print "Failed to write revar.py. ERROR: " + str(exc)
		sys.exit(1)


def gen_connection():
	try:
		f = open('connection.py', 'w')
		f.write("import socket")
		f.write("s = socket.socket(	)")
		f.write("commit = 'dev'")
		f.write("google_api = \"\"")
		f.write("personalityforge_api = \"\"")
		f.close()
	except BaseException as exc:
		print "Failed to generate connection.py. ERROR: " + str(exc)
		sys.exit(1)