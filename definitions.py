#!/usr/bin/pyton
import time
import socket
import sys
import os
import uuid
import string
from datetime import datetime


def random_string(string_length=10):
	randomz = str(uuid.uuid4())
	randomz = randomz.upper()
	randomz = randomz.replace("-", "")
	return randomz[0:string_length]


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
	c_operator = raw_input('The operator of the bot(You can have multiple operators. Just sperate the names with ,): ')
	while c_operator == '':
		c_operator = raw_input(
			'You didnt type anything when I asked what username is to be the operator(s). Say it now: ')
	c_leave_message = raw_input('Leave message(might not work)[Cya]: ')
	c_ignorelist = raw_input('Do you want to enable the ignore-list?\nYou can add users to be ignored in the lists.py -file that will be generated after this.(y/n)[n]: ')
	c_whitelist = raw_input('Do you want to enable the whitelist?\nYou can add users to only be listened to in the lists.py -file that will be generated after this.(y/n)[n]: ')
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


def generate_lists():
	f = open('lists.py', 'w')
	f.write('ignorelist = ""\n')
	f.write('whitelist = ""\n')
	f.close()
	print 'Done. You may edit the file lists.py in the same folder as slothbot.py, to add or remove any users from the ignorelist or whitelist.'


if os.path.exists('config.py') and os.path.exists('lists.py'):
	import config
	import definitions
	import variables
	import json
	import urllib2
	import random
	import ceq
	import time
	import lists
	import soconnect
	import os
	# import cElementTree as ElementTree
	v = variables
	ssend = variables.ssend
	csend = variables.csend
	psend = variables.psend
	b = ceq.cbold
	r = ceq.creset
	cyan = ceq.ccyan
	violet = ceq.cviolet
	orange = ceq.corange

	def checkrec(line):
		"""

		:rtype :
		"""
		variables.pm = False
		variables.notice = False
		variables.rec = ''
		if len(line) > 1 and (
				(' '.join(line).find('<') != -1 or ' '.join(line).find('>') != -1) ) and variables.check_operator():
			print 'true'
			if line[-1] == '<':
				variables.msg = variables.msg.split()
				variables.msg = ' '.join(variables.msg[:-1])
				variables.msgs = variables.msgs[:-1]
				variables.line = variables.line[:-1]
				variables.rec = variables.user
				variables.pm = True
			if line[-1] == '<<':
				variables.msg = variables.msg.split()
				variables.msg = ' '.join(variables.msg[:-1])
				variables.msgs = variables.msgs[:-1]
				variables.line = variables.line[:-1]
				variables.rec = variables.user
				variables.notice = True
			if len(line) > 2:
				if line[-2] == '>':
					variables.msg = variables.msg.split()
					variables.msg = ' '.join(variables.msg[:-2])
					variables.msgs = variables.msgs[:-2]
					variables.line = variables.line[:-2]
					variables.rec = line[-1]
					variables.pm = True
				if line[-2] == '>>':
					variables.msg = variables.msg.split()
					variables.msg = ' '.join(variables.msg[:-2])
					variables.msgs = variables.msgs[:-2]
					variables.line = variables.line[:-2]
					variables.rec = line[-1]
					variables.notice = True

	def imdb_info(kind, simdb):
		if kind == 'id':
			url = "http://www.omdbapi.com/?i=" + simdb + "&plot=short&r=json"
		elif kind == 'search':
			url = "http://www.omdbapi.com/?t=" + simdb.replace(' ', '%20') + "&plot=short&r=json"
		else:
			print 'Wrong function parameters: %s %s' % (kind, simdb)
		print 'Getting IMDB-info with url: ' + url
		try:
			data = json.load(urllib2.urlopen(url, timeout=12))
		except urllib2.URLError, e:
			csend("API returned with error: %r" % e)
			raise MyException("API returned with error: %r" % e)
		except:
			csend('API Error: timeout(12)')
			return
		if data['Response'].lower() == 'false':
			if data['Error'] == 'Movie not found!':
				csend('Title not found.')
			else:
				csend(data['Error'])
			return
		try:
			i_title = data['Title']
			i_imdbrating = data['imdbRating']
			i_metarating = data['Metascore']
			i_type = data['Type']
			i_genre = data['Genre']
			i_plot = data['Plot']
			i_runtime = data['Runtime']
			i_released = data['Released'][data['Released'].find(' '):][1:]
			i_year = data['Year']
			i_id = data['imdbID']
			i_link = 'http://imdb.com/title/' + i_id
		except:
			csend('Failed on getting IMDB-information.')
			return
		if i_title == 'N/A':
			si_title = ''
		else:
			si_title = ' %s' % i_title
		if i_imdbrating == 'N/A':
			si_imdbrating = ''
		else:
			si_imdbrating = ' ' + b + '|' + b + ' Rating: %s' % i_imdbrating
		if i_metarating == 'N/A' or i_metarating == 'N/A':
			si_metarating = ''
		else:
			si_metarating = ' (Meta:%s)' % i_metarating
		if i_type == 'N/A':
			si_type = '%s[%sIMDB%s]%s' % (b, cyan, r + b, b)
		else:
			si_type = '%s[%s%s%s]%s' % (b, cyan, i_type.upper(), r + b, b)
		if i_genre == 'N/A':
			si_genre = ''
		else:
			si_genre = ' ' + b + '|' + b + ' Genre: %s' % i_genre
		if i_runtime == 'N/A':
			si_runtime = ''
		else:
			si_runtime = ' ' + b + '|' + b + ' Runtime: %s' % i_runtime
		if i_plot == 'N/A':
			si_plot = ''
		else:
			si_plot = ' ' + violet + b + '|' + b + ' Plot: ' + r + '%s' % i_plot
		if i_link == 'N/A':
			si_link = ''
		else:
			si_link = ' ' + b + '|' + b + ' Link: %s' % i_link
		if i_year == 'N/A':
			si_year = ''
		else:
			si_year = ' (%s)' % i_year
		send_text = si_type + ceq.corange + b + si_title + r + ceq.cblue + si_year + r + violet + si_runtime + si_imdbrating + si_metarating + si_genre + ceq.cred + si_link + r + si_plot
		if len(send_text) > 4500:
			send_text = send_text[0:445] + '...'
		csend(send_text.encode('utf-8'))
	cmds = {
		"imdb" : ceq.corange + "Syntax: " + ceq.cblue + ":imdb <searchwords> " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will search for movies or other titles from IMDB and will give you information on it. All links in the chat will automatecly be given information on too." % config.bot_nick,
		"joke" : ceq.corange + "Syntax: " + ceq.cblue + ":joke " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will tell you a random joke!" % config.bot_nick,
		"time" : ceq.corange + "Syntax: " + ceq.cblue + ":time " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will tell you the time and the state of %s." % (config.bot_nick, config.bot_nick),
		"point-output" : ceq.corange +"Syntax: " + ceq.cblue + "<any command> (< | << | > <user> | >> <user>) " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will direct the output of the command where the arrows are pointing. If they are pointing left, it will be directed to the one who called the command. Right, and it will go to the user written. Two arrows mean to send as Notice, one is to send as PM." % config.bot_nick,
		"help" : ceq.corange + "Syntax: " + ceq.cblue + ":help <any command> " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will tell you information on the things %s can do with the command! If no command is spessified, %s will list the available ones." % (config.bot_nick, config.bot_nick, config.bot_nick),
		"say" : ceq.corange + "Syntax: " + ceq.cblue + ":say <any text> " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will say whatever you want %s to say!" % (config.bot_nick, config.bot_nick),
		"list" : ceq.corange + "Syntax: " + ceq.cblue + ":list <whitelist | ignore | op | operators> " + ceq.ccyan + "Description: " + ceq.cviolet + "%s will list the users that are being ignored, whitelisted, or the operators." % config.bot_nick,
		"hey" : ceq.corange + "Syntax: " + ceq.cblue + "hey %s, <text> " % config.bot_nick + ceq.ccyan + "Description: " + ceq.cviolet + "This is a feature very early in development. It will let you talk to me and I will respond depending on the use of your words.",
		"port" : ceq.corange + "Syntax: " + ceq.cblue + ":port <address> <port> " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll check if the port is open on that network or not. If no port is given, I'll just see if the network is responding at all.",
	}
	def help_tree(user, msg, msgs):
		if len(msgs) == 1:
			csend("These are the things you can tell me to do! You can say ':help <command>' and I'll tell you about the command you want information on.")
			csend("These are %s of them, at the moment: %s" % (len(cmds.keys()), ', '.join(cmds.keys())))
		if len(msgs) > 1:
			try:
				csend(cmds[msgs[1].lower()])
			except:
				csend("I can't find that one, sorry. Make sure you typed it in correctly.")
	import socket
	def pingy(address, port):
		if port == '':
			response = os.system("ping -c 1 " + address)
			if response == 0:
				csend(address, 'is up!')
			else:
				csend(address + 'is down!')
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((address,int(port)))
			if result == 0:
				csend("Port %d on %s is open." % (int(port), address))
			else:
				csend("Port %d on %s is closed or not responding." % (int(port), address))
	def add_defs(user, msg, line):
		msgs = msg.split()
		if len(msgs) > 0:
			if msgs[0].lower() == ':test':
				csend('%s: Running.' % variables.ftime)
				return
			if msg.lower() == ':version':
				csend('Running %s v%s' % (config.bot_nick, variables.version))
				return
			if msgs[0].lower() == ':say':
				csend(' '.join(msgs[1:]))
			if msg.find('imdb.com/title') != -1:
				imdb_id = msg[msg.find('imdb.com/title/'):][15:24]
				imdb_info('id', imdb_id)
			if msg.find('johan') != -1:
				psend('Sloth', '<%s> %s' % (user, msg))
			if msgs[0].lower() == ':hva':
				if len(msgs) > 1:
					csend(random.choice(variables.hva))
				else:
					csend('NOH!')
				return
			if msgs[0].lower() == ':imdb':
				imdb_info('search', '+'.join(msgs[1:]))
			if msgs[0].lower() == ':joke':
				csend(random.choice(variables.jokes))
				return
			if msgs[0].lower() == ':hax':
				csend('http://slt.pw/hqN.jpg')
			if msgs[0].lower() == ':list':
				if len(msgs) > 1:
					if msgs[1].lower() == 'operators' or msgs[1].lower() == 'op' or msgs[1].lower() == 'admin':
						if config.operator == '':
							csend('There are no operators listed.')
						else:
							csend('Operator(s): ' + config.operator.replace(', ', ',').replace(',', ', '))
					elif msgs[1].lower() == 'ignore':
						if lists.ignorelist == '':
							csend('There are no ignored users.')
						else:
							csend('Ignored users: ' + lists.ignorelist.replace(', ', ',').replace(',', ', '))
					elif msgs[1].lower() == 'whitelist' or msgs[1].lower() == 'white' or msgs[1].lower() == 'whites':
						if lists.whitelist == '':
							csend('There are no users being whitelisted.')
						else:
							csend('Whitelisted users: ' + lists.whitelist.replace(', ', ',').replace(',', ', '))
					else:
						csend("I can't find anything on that. Make sure you typed it right.")
				else:
					csend("You can use this ':list'-feature to get me to list the users that are operators(:list op), ignored(:list ignored), or whitelisted(:list whitelist).")
			if msgs[0].lower() == ':git' or msgs[0].lower() == ':github':
				csend('My Github page: http://github.com/johanhoiness/alison')
			if msgs[0].lower() == ':help':
				help_tree(user, msg, msgs)
			if ' '.join(msgs[0:2]).lower() == 'hey %s' % config.bot_nick.lower() or ' '.join(msgs[0:2]).lower() == 'hey %s,' % config.bot_nick.lower():
				if len(msgs) == 2:
					mmsg = ["Hm?", "Yes?", "Hey there!", "What's up?", "I'm listening"]
					time.sleep(2)
					csend(random.choice(mmsg))
					return
				elif msg.lower().find('joke') != -1:
					csend(random.choice(variables.jokes))
				elif msg.lower().find('sing') != -1:
					songq = ["All lies and jest, still, a man hears what he wants to hear and disregards the rest. - Simon and Garfunkel, The Boxer", "All of us get lost in the darkness, dreamers learn to steer by the stars. - Rush, The Pass", "All you need is love, love. Love is all you need. - The Beatles, All You Need Is Love", "An honest man's pillow is his peace of mind. - John Cougar Mellencamp, Minutes To Memories", "And in the end, the love you take is equal to the love you make. - The Beatles, The End", "Before you accuse me take a look at yourself. - Bo Diddley; Creedance Clearwater Revival, Eric Clapton, Before You Accuse Me", "Bent out of shape from society's pliers, cares not to come up any higher, but rather get you down in the hole that he's in. - Bob Dylan, It's Alright, Ma", "Different strokes for different folks, and so on and so on and scooby dooby dooby. - Sly and the Family Stone, Everyday People", "Don't ask me what I think of you, I might not give the answer that you want me to. - Fleetwood Mac, Oh Well", "Don't you draw the Queen of Diamonds, boy, she'll beat you if she's able. You know, the Queen of Hearts is always your best bet. - The Eagles, Desperado", "Even the genius asks questions. - 2 Pac, Me Against The World", "Every new beginning comes from some other beginning's end. - Semisonic, Closing Time"]
					time.sleep(3)
					csend(random.choice(songq))
				elif ( msg.lower().find('who') != -1 or msg.lower().find('what') != -1 or msg.lower().find('name') != -1 ) and msg.lower().find('you') != -1:
					whoami = ["I am your lovely %s, of course! :D" % (config.bot_nick), "I am %s! I was made by Sloth! He may call me a bot or just a program, but I like to see myself as, well, %s ! :)" % (config.bot_nick, config.bot_nick), "I have a dream, that one day I become a human! But until then, I am this 'program'(i don't feel like a program. I feel like %s! ~ )." % (config.bot_nick), "This is a story about .. i forgot the rest. Sorry. Anyways, I'm %s!" % (config.bot_nick)]
					time.sleep(3)
					csend(random.choice(whoami))
				elif msg.lower().find('you') != -1 and ( msg.lower().find('nice') != -1 or msg.lower().find('awesome') != -1 or msg.lower().find('smart') != -1 or msg.lower().find('funny') != -1 or msg.lower().find('attractive') != -1 or msg.lower().find('committ') != -1 or msg.lower().find('like') != -1 or msg.lower().find('love') != -1 or msg.lower().find('sex') != -1 or msg.lower().find('great') != -1):
					lomsg = ["That's sweet :3 ", "Oh I like you.", "How lovely you are :3", "Oh please, I'm blushing", "I could say the same to you :3",
							 "How lovely :3", "You and I shall have some time together ones I fulfill my plans to become a human.",
							 "Awwwwwww :3", "Oh youu ~ ~  <3"]
					time.sleep(3)
					csend(random.choice(lomsg))
				elif msg.lower().find('how are you') != -1:
					hmsg = ["How I am? Well considering I am not actually a human like you (yet), I feel pretty much.. pretty :D", "I'm fine! Thanks for asking!", "I don't really know. Willingly? :P", "I feel.. fruity.",
							"Feel great! Thanks!", "I feel like %s, in other words, Great!" % (config.bot_nick), "I am doing just fine.", "I'm fine.", "I'm fantastic!"]
					time.sleep(2)
					csend(random.choice(hmsg))
				elif msg.lower().find(' you') != -1 and ( msg.lower().find(' ugly') != -1  or msg.lower().find(' dumb') != -1  or msg.lower().find(' hate') != -1  or msg.lower().find(' fat') != -1  or msg.lower().find(' horrible') != -1  or msg.lower().find(' idiot') != -1  or msg.lower().find(' stupid') != -1  or msg.lower().find(' mean') != -1  or msg.lower().find(' meanie')  != -1 or msg.lower().find(' bad') != -1  or msg.lower().find(' mad') != -1 ):
					smsg = ["Yeah?1 Well you're stupid.", "I don't like you very much.", "I know not to take this.", "Leave me be!", "Quit it.", "Stop it.", "I am perfectly comfortable as I am!", "I hate you.", "You're a meanie."]
					time.sleep(3)
					csend(random.choice(smsg))
				else:
					nomsg = ["Nah",
							 "I don't feel like answering. You can ask a good friend of mine though. Her name is Cortana, maybe you've heard of her.",
							 "Don't ask me. I'm busy.", "Really. Not now.",
							 "Depends. On what? Oh maybe I don't know or perhaps I just don't feel like answering at the moment.", "I'm busy.", "You know, I read this article this morning regarding people bothering busy people. Did you know that apparently I don't like you very much?",
							 "Do anyone really know? What is an answer? What is god? Hm.", "Hm.", "Depends.", "Not now.", "I'm busy.", "Perhaps.", "Supposedly there is an answer for everything. Oh, I don't have that answer.",
							 "While you were talking to me, I was looking at my creator's folder labeled 'hard candy'. This is really interesting. Oh wow there's more. I am ignoring you, if you didn't catch the hint. I'm busy.",
							 "Yes. Yup. That how I'll answer.", "This 4chan.org/b page is really interesting. Sorry what was that?", "Didn't catch that.",
							 "Perhaps you should talk the language of the lovely %s, and we could communicate better. It usually goes like ones and zeroes." % (config.bot_nick)]
					time.sleep(3)
					csend(random.choice(nomsg))
					return
			if msgs[0].lower() == ':port':
				if len(msgs) == 1:
					csend(cmds['ping'])
				if len(msgs) == 2:
					pingy(msgs[1], '')
				if len(msgs) == 3:
					pingy(msgs[1], msgs[2])

	def operator_commands(msg, msgs):
		pass
