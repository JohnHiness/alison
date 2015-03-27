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


def generate_lists():
	f = open('revar.py', 'w')
	f.write('ignorelist = ""\n')
	f.write('whitelist = ""\n')
	f.close()
	print 'Done. You may edit the file revar.py in the same folder as slothbot.py, to add or remove any users from the ignorelist or whitelist.'


if os.path.exists('config.py') and os.path.exists('revar.py'):
	import config
	import definitions
	import variables
	import json
	import urllib2
	import random
	import ceq
	import time
	import revar
	import soconnect
	import os
	import time
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
				(' '.join(line).find('<') != -1 or ' '.join(line).find('>') != -1) ):
			if not revar.outputredir_all:
				if not variables.check_operator():
					return
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

	def shorten_url(url):
		post_url = 'https://www.googleapis.com/urlshortener/v1/url?&key=' + variables.google_api
		postdata = {'longUrl':url,
					'key':variables.google_api}
		headers = {'Content-Type':'application/json'}
		req = urllib2.Request(
			post_url,
			json.dumps(postdata),
			headers
		)
		ret = urllib2.urlopen(req).read()
		return json.loads(ret)['id']
	def refresh_version():
		url7 = "https://api.github.com/repos/johanhoiness/alison/commits"
		data7 = json.load(urllib2.urlopen(url7, timeout=4))
		if data7[0]['commit']['url'][data7[0]['commit']['url'].find('commits/') + 8 :][:7] != '':
			revar.commit = data7[0]['commit']['url'][data7[0]['commit']['url'].find('commits/') + 8 :][:7]
	def get_hash(chan, imdb_id):
		try:
			variables.torrent_hash = ''
			if not revar.get_hash:
				return
			url3 = "https://yts.to/api/v2/list_movies.json?query_term=" + imdb_id
			data3 = json.load(urllib2.urlopen(url3, timeout=8))
			quality1080 = ''
			quality720 = ''
			for torrent in data3['data']['movies'][0]['torrents']:
				if torrent['quality'] == '1080p':
					quality1080 = torrent['hash']
				elif torrent['quality'] == '720p':
					quality720 = torrent['hash']
				else:
					noquality = [torrent['hash'], torrent['quality']]
			if quality1080 != '':
				quality = '1080p'
				xhash = quality1080
			elif quality720 != '':
				quality = '720p'
				xhash = quality720
			else:
				quality = noquality[1]
				xhash = noquality[0]
			variables.torrent_hash = xhash
		except BaseException as exc:
			if revar.dev:
				print 'Failed to get Torrent information, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, "Error in variables.get_hash(), line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
			else:
				csend(chan, "Something went wrong getting torrent hash.")
	def imdb_info(chan, kind, simdb):
		if kind == 'id':
			url = "http://www.omdbapi.com/?i=" + simdb + "&plot=short&r=json"
#		elif kind == 'search':
#			url = "http://www.omdbapi.com/?t=" + simdb.replace(' ', '%20') + "&plot=short&r=json"
		elif kind == 'search':
			url2 = "http://www.imdb.com/xml/find?json=1&q=" + simdb
			try:
				data2 = json.load(urllib2.urlopen(url2, timeout=8))
				try:
					if len(data2["title_popular"]) < 1:
						csend(chan, "Title not found.")
						return
				except:
					csend(chan, "Title not found.")
					return
				url = "http://www.omdbapi.com/?i=" + data2["title_popular"][0]["id"]
			except:
				url = "http://www.omdbapi.com/?t=" + simdb
#				csend(chan, "IMDB-API not respoding (timeout after 8 sec)")
#				return

		else:
			print 'Wrong function parameters: %s %s' % (kind, simdb)
		print 'Getting IMDB-info with url: ' + url
		try:
			data = json.load(urllib2.urlopen(url, timeout=12))#
		except urllib2.URLError, e:
			if revar.dev:
				csend(chan, "API returned with error: %r" % e)
			else:
				csend(chan, "Something went wrong requesting information.")
			return
		except:
			csend(chan, 'API Error: timeout(12)')
			return
		if data['Response'].lower() == 'false':
			if data['Error'] == 'Movie not found!':
				csend(chan, 'Title not found.')
			else:
				csend(chan, data['Error'])
			return

		try:
			print data
			i_id = data['imdbID']
			i_link = shorten_url('http://imdb.com/title/' + i_id)[7:]
			get_hash(chan, data['imdbID'])
			i_title = data['Title']
			i_imdbrating = data['imdbRating']
			i_metarating = data['Metascore']
			i_type = data['Type']
			i_genre = data['Genre']
			i_plot = data['Plot']
			i_runtime = data['Runtime']
			i_released = data['Released'][data['Released'].find(' '):][1:]
			i_year = data['Year']
		except BaseException as exc:
			if revar.dev:
				print 'Failed to get torrent information, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, "Error in variables.imdb_info() getting information from array, line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
			else:
				csend(chan, "Something went wrong when getting IMDB-information.")
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
		if variables.torrent_hash != '':
			si_magnet = ' ' + b + '|' + b + ' YIFY-Torrent: %s' % shorten_url('https://yts.re/torrent/download/' + variables.torrent_hash + '.torrent').replace('http://', '')
		else:
			si_magnet = ''
		send_text = si_type + ceq.corange + b + si_title + r + ceq.cblue + si_year + r + violet + si_runtime + si_imdbrating + si_metarating + si_genre + ceq.cred + si_link + si_magnet + r + si_plot
		if len(send_text) > 4500:
			send_text = send_text[0:445] + '...'
		csend(chan, send_text.encode('utf-8'))
	cmds = {
		"imdb" : ceq.corange + "Syntax: " + ceq.cblue + "imdb <searchwords> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will search for movies or other titles from IMDB and will give you information on it. All links in the chat will automatecly be given information on too.",
		"joke" : ceq.corange + "Syntax: " + ceq.cblue + "joke " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you a random joke!" ,
		"test" : ceq.corange + "Syntax: " + ceq.cblue + "time " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you the time and the state of myself.",
		"point-output" : ceq.corange +"Syntax: " + ceq.cblue + "<any command> (< | << | > <user> | >> <user>) " + ceq.ccyan + "Description: " + ceq.cviolet + "I will direct the output of the command where the arrows are pointing. If they are pointing left, it will be directed to the one who called the command. Right, and it will go to the user written. Two arrows mean to send as Notice, one is to send as PM.",
		"help" : ceq.corange + "Syntax: " + ceq.cblue + "help <any command> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you information on the things I can do with the command! If no command is spessified, I will list the available ones.",
		"say" : ceq.corange + "Syntax: " + ceq.cblue + "say <any text> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will say whatever you want me to say!",
		"list" : ceq.corange + "Syntax: " + ceq.cblue + "list <whitelist | ignore | op | operators> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will list the users that are being ignored, whitelisted, or the operators.",
		"hey" : ceq.corange + "Syntax: " + ceq.cblue + "hey %s, <text> " % revar.bot_nick + ceq.ccyan + "Description: " + ceq.cviolet + "This is a feature very early in development. It will let you talk to me and I will respond depending on the use of your words.",
		"port" : ceq.corange + "Syntax: " + ceq.cblue + "port <address> <port> " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll check if the port is open on that network or not. If no port is given, I'll just see if the network is responding at all.",
		"bing" : ceq.corange + "Syntax: " + ceq.cblue + "bing <searchwords> " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll give you a link to the searchresults from the greatest search-engine of all time using your searchwords!",
		"time" : ceq.corange + "Syntax: " + ceq.cblue + "time " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll give you the full time! Oh and I won't allow you to give any parameters. Standardization, yo!",
		"weather" : ceq.corange + "Syntax: " + ceq.cblue + "weather <location| > " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll tell you the weather and temperature of the given location. If no location is spesified, it will choose the default location which currently is set to %s." % revar.location,
		"operator-commands" : ceq.corange + "Syntax: " + ceq.cblue + "{0}<:|,| > <any operator-command>".format(revar.bot_nick) + ceq.ccyan + " Description: " + ceq.cviolet + "This is only accessable for operators. See \"$BOTNICK<:|,| > help\" for more information on this feature. All non-operators will be ignored calling a command this way.",
	}
	def help_tree(chan, user, msg, msgs):
		if len(msgs) == 1:
			csend(chan, "These are the things you can tell me to do! You can say ':help <command>' and I'll tell you about the command you want information on.")
			csend(chan, "These are %s of them, at the moment: %s" % (len(cmds.keys()), ', '.join(cmds.keys())))
		if len(msgs) > 1:
			try:
				csend(chan, cmds[msgs[1].lower()])
			except:
				csend(chan, "I can't find that one, sorry. Make sure you typed it in correctly.")
	import socket

	weather_codes = {
		200:"There is a bloody light thundarrstorm on the way",
		201:"There is a bloody thundarrstorm on the way",
		202:"There is a bloody heavy thundarrstorm on the way",
		210:"Light thunderstorm on the loose",
		211:"THUNDARR",
		212:"Beware, beware. There's heavy thunderstorm about",
		221:"Raggidy ragged thunderstorm",
		230:"Thundar with a little drizzily rain",
		231:"Thundar with drizzle",
		232:"Thundarstorm with a heavy drizzle",
		300:"Light dense drizzzle",
		301:"Drizzely drizzle",
		302:"The drizzle is heavy with this one",
		310:"Light intensity drizzely rain",
		311:"Drizzely rain",
		312:"Heavy intensity drizzely rain",
		313:"It's showerin raiiin",
		314:"It's showerin heavy",
		321:"Drizzely shower",
		500:"Lighty light rain",
		501:"Moderetly rainy rain",
		502:"The rain is intense",
		503:"The rain is VERY intense",
		504:"EXTREME RAIN",
		511:"Freezin rain",
		520:"Lighty dense rain",
		521:"Showerin rain",
		522:"Dense shower rain",
		531:"Raggedy showerin rain",
		600:"Lightly crystalized dihydrogenmonoxide",
		601:"Raining crystalized dihydrogenmonoxide",
		602:"Heavy raining crystalized dihydrogenmonoxide",
		611:"Sleetly raining crystalized dihydrogenmonoxide",
		612:"Showring dihydrogenmonoxide crystals",
		615:"Lightly raining dihydrogenmonoxide- crystalized and not",
		616:"Raining dihydrogenmonoxide- crystalized and not",
		620:"Lightly showring crystalized dihydrogenmonoxide",
		621:"Showering crystalized dihydrogenmonoxide",
		622:"Heavely showering crystalized dihydrogenmonoxide",
		701:"The clouds are attacking",
		711:"Throwing Smoke!",
		721:"It's hazy",
		731:"Quite dusty",
		741:"The clouds are attacking",
		751:"The sandy sands are invading",
		761:"de_dust",
		762:"Filled with carbon from a volcano",
		771:"It's squallin",
		781:"A tornado is being a tornado",
		800:"If you look up you'll see nothing but the upper atmosphere",
		801:"Some collections of dihydromonoxide can be seen floating in the sky",
		802:"Scattered clouds can be seen in the sky",
		803:"Broken clouds can be seen in the sky",
		804:"Overcast clouds in the sky",
		900:"idk something about a tornado",
		901:"A tropical storm",
		902:"Hurricane, yo",
		903:"It'z freeezzzin",
		904:"It's so haht",
		905:"Quite windy",
		906:"It's hailin'",
		951:"The air is calm",
		952:"It's a litey breeze",
		953:"It's a gentlebreeze",
		954:"It's a moderatly tense breeze",
		955:"It's a freshy breeze",
		956:"The breeze is strong",
		957:"The wind is tall with a near gale",
		958:"It's gale",
		959:"It's severe gale",
		960:"A Storm of Destiny",
		961:"It's a bloody violent storm",
		962:"A bloody huricane",

		## For information on the weathercodes: http://openweathermap.org/weather-conditions

	}
	def weather(chan, location=revar.location, allchan=False):
		try:
			location = location.split()
			url5 = "http://api.openweathermap.org/data/2.5/weather?q={0}&mode=json".format(str('+'.join(location)))
			data5 = json.load(urllib2.urlopen(url5, timeout=8))
			if config.verbose:
				print data5
			if data5['cod'] == '404':
				csend(chan, "Location not found.")
				return ''
			if data5['cod'] != 200:
				csend(chan, 'Error in request.')
				return ''
			if revar.weather_custom and data5['weather'][0]['id'] in weather_codes.keys():
				w_desc = weather_codes[data5['weather'][0]['id']]
			else:
				w_desc = data5['weather'][0]['description']
			w_temp = data5['main']['temp'] - 273.15
			w_country = data5['sys']['country']
			w_wind = data5['wind']['speed']
			if w_country == '':
				csend(chan, "Location not found.")
				return ''
			w_city = data5['name']
			text_to_send = "{0}Forecast of {3}{4}{0}, {1}{2}{0}: {11}{6}{0}, {10}with a temperature of {7}{8}{10}&DEGREE; celsius and a windspeed of {7}{9}{10} m/s.".format(ceq.cblue, ceq.cred, w_country.encode('utf-8'), ceq.cviolet, w_city.encode('utf-8'), ceq.ccyan, w_desc, ceq.corange, w_temp, w_wind, ceq.clcyan, ceq.cgreen)
			return text_to_send
		except BaseException as exc:
			if revar.dev:
				outp = "Error in variables.weather(), line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				print outp
				if allchan:
					variables.ssend("PRIVMSG {0} :".format(','.join(revar.channels)) + outp)
				else:
					csend(chan, outp)
				return ''
			else:
				if allchan:
					variables.ssend("PRIVMSG {0} :".format(','.join(revar.channels)) + "Something went wrong getting the weather.")
				else:
					csend(chan, "Something went wrong getting the weather.")
				return ''

	def pingy(chan, address, port):
		if port == '':
			response = os.system("ping -c 1 -W 8 " + address)
			if response == 0:
				csend(chan, address + ' is up!')
			else:
				csend(chan, address + ' is down!')
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(5)
			result = sock.connect_ex((address,int(port)))
			if result == 0:
				csend(chan, "Port %d on %s is open." % (int(port), address))
			else:
				csend(chan, "Port %d on %s is closed or not responding." % (int(port), address))

	operator_cmds = dict(
		op=ceq.corange + "Syntax: " + ceq.cblue + "op <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will make the user an operator.",
		deop=ceq.corange + "Syntax: " + ceq.cblue + "deop <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will remove operator-rights from user.",
		config=ceq.corange + "Syntax: " + ceq.cblue + "config <set|save>" + ceq.ccyan + " Description: " + ceq.cviolet + "This is to edit many variables in the bot. Use \"config set\" to view them. All the variables can also be permanetly saved by using \"save\" instead of \"set\".",
		nick=ceq.corange + "Syntax: " + ceq.cblue + "nick <new nickname>" + ceq.ccyan + " Description: " + ceq.cviolet + "Change the nickname of the bot.",
		whitelist=ceq.corange + "Syntax: " + ceq.cblue + "whitelist <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will add the user to the whitelist, making them unignoreable when whitelisting is set to True.",
		ignore=ceq.corange + "Syntax: " + ceq.cblue + "ignore <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will add the user to the ignorelist, making them unnoticeable by the bot.",
		mute=ceq.corange + "Syntax: " + ceq.cblue + "mute" + ceq.ccyan + " Description: " + ceq.cviolet + "Will mute the output no matter what.",
		unmute=ceq.corange + "Syntax: " + ceq.cblue + "<umute|unmute>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will unmute the output.",
		unwhitelist=ceq.corange + "Syntax: " + ceq.cblue + "<unwhitelist|unwhite|niggerfy> <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will remove user from whitelist.",
		unignore=ceq.corange + "Syntax: " + ceq.cblue + "unignore <user>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will remove user from ignorelist.",
		restart=ceq.corange + "Syntax: " + ceq.cblue + "restart" + ceq.ccyan + " Description: " + ceq.cviolet + "Will simply restart the bot.",
		compile=ceq.corange + "Syntax: " + ceq.cblue + "compile" + ceq.ccyan + " Description: " + ceq.cviolet + "Will compile all the files the bot needs to run. This will make the bot run remarkably faster.",
		join=ceq.corange + "Syntax: " + ceq.cblue + "join <channel>" + ceq.ccyan + " Description: " + ceq.cviolet + "Bot will join the given channel(s).",
		part=ceq.corange + "Syntax: " + ceq.cblue + "part <|channel>" + ceq.ccyan + " Description: " + ceq.cviolet + "Bot will part from the given channel(s). If no channel is spessified, it will part with the channel the command was triggered from.",
		quit=ceq.corange + "Syntax: " + ceq.cblue + "quit" + ceq.ccyan + " Description: " + ceq.cviolet + "Bot will simply kill it's process.",
		update=ceq.corange + "Syntax: " + ceq.cblue + "quit" + ceq.ccyan + " Description: " + ceq.cviolet + "Bot will update certain modules.",
		git_update=ceq.corange + "Syntax: " + ceq.cblue + "git-update" + ceq.ccyan + " Description: " + ceq.cviolet + "Bot will pull the lastst commit from git, and reboot.")


	def save_revar(chan):
		try:
			dict_of_var = {
				'midsentence_comment':revar.midsentence_comment, 'midsentence_trigger':revar.midsentence_trigger, 'outputredir_all':revar.outputredir_all, 'outputredir':revar.outputredir, 'ignorelist':revar.ignorelist, 'whitelist':revar.whitelist, 'ignorelist_set':revar.ignorelist_set, 'whitelist_set':revar.whitelist_set, 'end_triggers':revar.end_triggers, 'triggers':revar.triggers, 'get_hash':revar.get_hash, 'bot_nick':"\""+revar.bot_nick+"\"", 'operators':revar.operators, "channels":revar.channels, "dev":revar.dev, "location":"\""+revar.location+"\"", "autoweather":revar.autoweather, "autoweather_time":revar.autoweather_time, "weather_custom":revar.weather_custom, "commit":revar.commit,
			}
			#os.rename( "revar.py", "revar.bak" )
			with open( "revar.py", "w" ) as target:
				for variable_name in dict_of_var:
					target.write("{0} = {1}\n".format(variable_name, dict_of_var[variable_name]))
				target.close()
			return True
		except BaseException as exc:
			if revar.dev:
				print 'Failed to save to file, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, "Error in when trying to rewrite revar.py, line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
			else:
				csend(chan, "Something went wrong trying to save.")
			return False

	def operator_commands(chan, msgs):
		try:
			print 'Configuration call - detected: ' + str(msgs)
			variable_list = [
				"{0:s}triggers({1:s}string={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, revar.triggers),
				"{0:s}ignorelist({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.ignorelist_set)),
				"{0:s}whitelist({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.whitelist_set)),
				"{0:s}commentchar({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.midsentence_comment)),
				"{0:s}midsentence_trigger({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.midsentence_trigger)),
				"{0:s}point-output({1:s}on(true)/off(false)={2:s}{3:s}{1:s}, all(true)/op(false)={2:s}{4:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.outputredir), str(revar.outputredir_all)),
	            "{0:s}get_hash({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.get_hash)),
	            "{0:s}dev({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.dev)),
	            "{0:s}location({1:s}string={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.location)),
				"{0:s}autoweather({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.autoweather)),
				"{0:s}autoweather_time({1:s}int={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.autoweather_time)),
				"{0:s}weather_custom({1:s}bool={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.weather_custom)),
			#   "{0:s}variable({1:s}string={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, ),
			]
			if (len(msgs) > 1) and msgs[0].lower() == 'ignore':
				revar.ignorelist.append(msgs[1])
				csend(chan, 'Ignoring user %s.' % msgs[1])
			if (len(msgs) == 2) and msgs[0].lower() == 'unignore':
				try:
					revar.ignorelist.remove(msgs[1])
					csend(chan, "No longer ignoring user '%s'" % msgs[1])
				except:
					csend(chan, "Ignored user was not found. Make sure you typed it in correctly.")
			if (len(msgs) > 1) and (msgs[0].lower() == 'whitelist' or msgs[0].lower() == 'white'):
				revar.whitelist.append(msgs[1])
				csend(chan, 'User %s is now whitelisted' % msgs[1])
			if (len(msgs) == 2) and (msgs[0].lower() == 'unwhitelist' or msgs[0].lower() == 'un;white' or msgs[0].lower() == 'niggerfy'):
				try:
					revar.whitelist.remove(msgs[1])
					csend(chan, "User '%s' no longer whitelisted" % msgs[1])
				except:
					csend(chan, "Whitelisted user was not found. Make sure you typed it in correctly.")
			if len(msgs) > 0 and msgs[0].lower() == 'config':
				if len(msgs) > 1:
					if msgs[1].lower() == 'set':
						if len(msgs) == 2:
							csend(chan, ceq.cred + "Variables: " + ', '.join(variable_list))
							return
						if msgs[2].lower() == 'triggers':
							if len(msgs) > 3:
								revar.triggers = (' '.join(msgs[3:]).replace(', ', '||')).lower().replace('"', '').replace('$botnick', revar.bot_nick.lower()).split('||')
								print (' '.join(msgs[3:]).replace(', ', '||'))
								print revar.triggers
								csend(chan, 'New triggers: ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"')
							else:
								csend(chan, 'Current triggers(use same format when setting): ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"')
						if msgs[2].lower() == 'location':
							if len(msgs) > 3:
								revar.location = msgs[3]
								csend(chan, 'New location: ' + ceq.cred + revar.location)
							else:
								csend(chan, 'Current location: ' + ceq.cred + revar.location)
						if msgs[2].lower() == 'ignorelist' or msgs[2].lower() == 'ignore':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.ignorelist_set = True
									csend(chan, 'Ignorelist set to True. I will now ignore any users on that list.')
								elif msgs[3].lower() == 'false':
									revar.ignorelist_set = False
									csend(chan, 'Ignorelist set to False. I will no longer ignore any users that are on the ignorelist.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the ignore-feature. Default is Off. Use "config set ignorelist <true|false>" to set.')
						if msgs[2].lower() == 'whitelist' or msgs[2].lower() == 'white':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.whitelist_set = True
									csend(chan, 'Whitelist set to True. I will now ignore any users NOT on that list.')
								elif msgs[3].lower() == 'false':
									revar.whitelist_set = False
									csend(chan, 'Whitelist set to False. I will no longer ignore any users that aren\'t on the whitelist.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the whitelist-feature. Default is Off. Use "config set whitelist <true|false>" to set.')
						if msgs[2].lower() == 'commentchar' or msgs[2].lower() == 'comment':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.midsentence_comment = True
									csend(chan, 'Midsentence_comment set to True.')
								elif msgs[3].lower() == 'false':
									revar.midsentence_comment = False
									csend(chan, 'Midsentence_comment set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the midsentence-commentout-feature. Default is Onn. Use "config set commentchar <true|false>" to set.')
						if msgs[2].lower() == 'weather_custom':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.weather_custom = True
									csend(chan, 'Weather_custom set to True.')
								elif msgs[3].lower() == 'false':
									revar.weather_custom = False
									csend(chan, 'Weather_custom set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable custom weather descriptions.')

						if msgs[2].lower() == 'commentchar' or msgs[2].lower() == 'comment':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.midsentence_comment = True
									csend(chan, 'Midsentence_comment set to True.')
								elif msgs[3].lower() == 'false':
									revar.midsentence_comment = False
									csend(chan, 'Midsentence_comment set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the midsentence-commentout-feature. Default is Onn. Use "config set commentchar <true|false>" to set.')

						if msgs[2].lower() == 'dev':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.dev = True
									csend(chan, 'Dev set to True.')
								elif msgs[3].lower() == 'false':
									revar.dev = False
									csend(chan, 'Dev set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable certain failsafes, making the bot less stabel but outputs better error-messages. Default is False. Use "config set dev <true|false>" to set.')
						if msgs[2].lower() == 'midsentence_trigger' or msgs[2].lower() == 'midtrigger':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.midsentence_trigger = True
									csend(chan, 'Midsentence_trigger set to True.')
								elif msgs[3].lower() == 'false':
									revar.midsentence_trigger = False
									csend(chan, 'Midsentence_trigger set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the midsentence-trigger-feature. Type ":(<command>)" in any part of the message to trigger commands. Default is Off. Use "config set commentchar <true|false>" to set.')
						if msgs[2].lower() == 'autoweather' or msgs[2].lower() == 'autoweather':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.autoweather = True
									csend(chan, 'Autoweather set to True.')
								elif msgs[3].lower() == 'false':
									revar.autoweather = False
									csend(chan, 'Autoweather set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable the automatic forecast.')
						if msgs[2].lower() == 'get_hash':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.get_hash = True
									csend(chan, 'Get_hash set to True.')
								elif msgs[3].lower() == 'false':
									revar.get_hash = False
									csend(chan, 'Get_hash set to False.')
								else:
									csend(chan, 'Use "true" or "false".')
							else:
								csend(chan, 'Enable or disable IMDB from trying to get hash/torrents (quickens response time). Default is True. Use "config set get_char <true|false>" to set.')
						if msgs[2].lower() == 'autoweather_time':
							if len(msgs) > 3:
								if not msgs[3].isdigit():
									csend(chan, 'Variable must be numbers only')
									return
								if not len(msgs[3]) == 4:
									csend(chan, 'You must use 4 digits for this variable.')
									return
								revar.autoweather_time = int(msgs[3])
								csend(chan, 'New autoweather_time: ' + str(revar.autoweather_time))
							else:
								csend(chan, 'Change what time the autoweather should trigger. Format is digits only, as HHSS.')


						if msgs[2].lower() == 'point-output' or msgs[2].lower() == 'outputredir':
							if len(msgs) > 3:
								if msgs[3].lower() == 'true':
									revar.outputredir = True
									csend(chan, 'Point-output set to On.')
								elif msgs[3].lower() == 'false':
									revar.outputredir = False
									csend(chan, 'Point-output set to Off.')
								elif msgs[3].lower() == 'all':
									revar.outputredir_all = True
									csend(chan, 'Point-output set to available for all.')
								elif msgs[3].lower() == 'ops' or msgs[3].lower() == 'op':
									revar.outputredir_all = False
									csend(chan, 'Point-output set to available only for operators.')
								else:
									csend(chan, 'Use "true", "all", "ops" or "false".')
							else:
								csend(chan, 'Enable or disable the point-output feature. See "help point-output". Default is True, for only ops. Use "config set point-output <all|ops|true|false>" to set.')
					if msgs[1].lower() == 'save':
						if save_revar(chan):
							csend(chan, "Configurations successfully saved to file.")
				else:
					csend(chan, 'Here you can edit configurations and other variables of the bot. From here you can either "set" or "save". By setting you are changing the current bot, and by saving you are changing files of the bot - making the configuration permanent.')

			if len(msgs) > 0 and msgs[0].lower() == 'op':
				if len(msgs) > 1:
					revar.operators.append(msgs[1].lower())
					csend(chan, "User '%s' is now an operator." % msgs[1])
				else:
					csend(chan, 'Usage: "op <nick>".')
			if len(msgs) > 0 and msgs[0].lower() == 'nick':
				ssend("NICK " + msgs[1])
				ssend("TIME")
				variables.nick_call_channel = chan
				revar.bot_nick = msgs[1]
			if msgs[0].lower() == 'git-update':
				print 'Pulling from Git and updating...'
				try:
					url4 = "https://api.github.com/repos/johanhoiness/alison/commits"
					data4 = json.load(urllib2.urlopen(url4, timeout=4))
					csend(chan, ceq.ccyan + 'Last commit: ' + ceq.cviolet + data4[0]['commit']['message'].encode('utf-8'))

				except:
					print 'Failed to get commit-message from git.'

				try:
					outp = os.system("git pull http://github.com/johanhoiness/alison")
					if outp != 0:
						csend(chan, "Update failed.")
						return
					outp2 = os.system("python -O -m py_compile alison.py definitions.py variables.py config.py ceq.py revar.py soconnect.py")
					if outp2 != 0:
						csend(chan, "Download was successful but the compilation failed.")
						return
					try:
						#revar = reload(revar)
						#refresh_version()
						#save_revar(chan)
						pass
					except:
						csend(chan, "Failed writing to file. Make sure the program has permissions to the folder.")
						return
					csend(chan, 'Successfully installed. Restarting..')
					ssend('QUIT ' + config.leave_message)
					python = sys.executable
					print str(python)+'||'+str(python)+'||'+ str(* sys.argv)
					os.execl(python, python, * sys.argv)
					csend(chan, 'Done')
				except:
					csend(chan, 'Download or installation failed.')
			if len(msgs) > 0 and msgs[0].lower() == 'deop':
				if len(msgs) > 1:
					try:
						revar.operators.remove(msgs[1].lower())
						csend(chan, "User '%s' is no longer an operator." % msgs[1])
					except:
						csend(chan, "Operator not found. Make sure you typed it in correctly.")
				else:
					csend(chan, 'Usage: "deop <nick>".')
			if len(msgs) > 0 and msgs[0].lower() == 'help':
				if len(msgs) > 1:
					try:
						csend(chan, operator_cmds[msgs[1].lower()])
					except:
						csend(chan, "Command or function not found. Make sure you typed it in correctly.")
				else:
					csend(chan, "This help is for operator- commands and functions. There are currently %d of them. To use any of them, they must start by saying \"%s\" first, and can only be accessed by operators. To get more information on the command/function, use \"help <command>\"." % (len(operator_cmds), revar.bot_nick))
					csend(chan, "These are the ones available: " + ', '.join(operator_cmds.keys()))
			if len(msgs) > 0 and msgs[0] == 'save':
				csend(chan, "All configurations can be saved by using \"config save\".")
			if len(msgs) == 0:
				csend(chan, "All commands launched this way is for operators only. It is only to edit settings and variables. See \"%s: help\" for more information." % revar.bot_nick)
		except BaseException as exc:
			if revar.dev:
				print 'Error in definitions.operator_commands(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, "Error in definitions.operator_commands(), line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
			else:
				csend(chan, "Something went wrong processing operator command.")

	def add_defs(chan, user, msg, line):
		try:
			# global msgs
			msgs = msg.split()
			if len(msgs) > 0:
				if variables.check_trigger(msgs, 'test'):
					csend(chan, '%s: Running.' % variables.ftime)
				if variables.check_trigger(msgs, 'version'):
					csend(chan, 'Running %s v%s' % (revar.bot_nick, variables.version))
				if variables.check_trigger(msgs, 'say'):
					csend(chan, ' '.join(msgs[1:]))
				if msg.find('imdb.com/title') != -1:
					imdb_id = msg[msg.find('imdb.com/title/'):][15:24]
					imdb_info(chan, 'id', imdb_id)
				if msg.find('johan') != -1 or msg.find('slut') != -1:
					ssend('PRIVMSG Sloth :<%s> %s' % (user, msg))
				if variables.check_trigger(msgs, "hva"):
					if len(msgs) > 1:
						csend(chan, random.choice(variables.hva))
					else:
						csend(chan, 'NOH!')
					return
				if variables.check_trigger(msgs, "imdb"):
					imdb_info(chan, 'search', '+'.join(msgs[1:]))
				if variables.check_trigger(msgs, "joke"):
					csend(chan, random.choice(variables.jokes))
					return
				if variables.check_trigger(msgs, "hax"):
					csend(chan, 'http://slt.pw/hqN.jpg')
				if variables.check_trigger(msgs, "list"):
					if len(msgs) > 1:
						if msgs[1].lower() == 'operators' or msgs[1].lower() == 'op' or msgs[1].lower() == 'admin':
							if revar.operators == '':
								csend(chan, 'There are no operators listed.')
							else:
								csend(chan, 'Operator(s): ' + ceq.cred + ', '.join(revar.operators))
						elif msgs[1].lower() == 'ignore' or msgs[1].lower() == 'ignored' or msgs[1].lower() == 'ignorelist':
							if revar.ignorelist == []:
								csend(chan, 'There are no ignored users.')
							else:
								csend(chan, 'Ignored users: ' + ', '.join(revar.ignorelist))
						elif msgs[1].lower() == 'whitelist' or msgs[1].lower() == 'white' or msgs[1].lower() == 'whites':
							if revar.whitelist == []:
								csend(chan, 'There are no users being whitelisted.')
							else:
								csend(chan, 'Whitelisted users: ' + ', '.join(revar.whitelist))
						else:
							csend(chan, "I can't find anything on that. Make sure you typed it right.")
					else:
						csend(chan, "You can use this ':list'-feature to get me to list the users that are operators(:list op), ignored(:list ignore), or whitelisted(:list whitelist).")
				if variables.check_trigger(msgs, "git") or variables.check_trigger(msgs, "github"):
					csend(chan, 'My Github page: http://github.com/johanhoiness/alison')
				if variables.check_trigger(msgs, "help"):
					help_tree(chan, user, msg, msgs)
				if ' '.join(msgs[0:2]).lower() == 'hey %s' % revar.bot_nick.lower() or ' '.join(msgs[0:2]).lower() == 'hey %s,' % revar.bot_nick.lower():
					if len(msgs) == 2:
						mmsg = ["Hm?", "Yes?", "Hey there!", "What's up?", "I'm listening"]
						time.sleep(2)
						csend(chan, random.choice(mmsg))
						return
					elif msg.lower().find('joke') != -1:
						csend(chan, random.choice(variables.jokes))
					elif msg.lower().find('sing') != -1:
						songq = ["All lies and jest, still, a man hears what he wants to hear and disregards the rest. - Simon and Garfunkel, The Boxer", "All of us get lost in the darkness, dreamers learn to steer by the stars. - Rush, The Pass", "All you need is love, love. Love is all you need. - The Beatles, All You Need Is Love", "An honest man's pillow is his peace of mind. - John Cougar Mellencamp, Minutes To Memories", "And in the end, the love you take is equal to the love you make. - The Beatles, The End", "Before you accuse me take a look at yourself. - Bo Diddley; Creedance Clearwater Revival, Eric Clapton, Before You Accuse Me", "Bent out of shape from society's pliers, cares not to come up any higher, but rather get you down in the hole that he's in. - Bob Dylan, It's Alright, Ma", "Different strokes for different folks, and so on and so on and scooby dooby dooby. - Sly and the Family Stone, Everyday People", "Don't ask me what I think of you, I might not give the answer that you want me to. - Fleetwood Mac, Oh Well", "Don't you draw the Queen of Diamonds, boy, she'll beat you if she's able. You know, the Queen of Hearts is always your best bet. - The Eagles, Desperado", "Even the genius asks questions. - 2 Pac, Me Against The World", "Every new beginning comes from some other beginning's end. - Semisonic, Closing Time"]
						time.sleep(3)
						csend(chan, random.choice(songq))
					elif ( msg.lower().find('who') != -1 or msg.lower().find('what') != -1 or msg.lower().find('name') != -1 ) and msg.lower().find('you') != -1:
						whoami = ["I am your lovely %s, of course! :D" % (revar.bot_nick), "I am %s! I was made by Sloth! He may call me a bot or just a program, but I like to see myself as, well, %s ! :)" % (revar.bot_nick, revar.bot_nick), "I have a dream, that one day I become a human! But until then, I am this 'program'(i don't feel like a program. I feel like %s! ~ )." % (revar.bot_nick), "This is a story about .. i forgot the rest. Sorry. Anyways, I'm %s!" % (revar.bot_nick)]
						time.sleep(3)
						csend(chan, random.choice(whoami))
					elif msg.lower().find('you') != -1 and ( msg.lower().find('nice') != -1 or msg.lower().find('awesome') != -1 or msg.lower().find('smart') != -1 or msg.lower().find('funny') != -1 or msg.lower().find('attractive') != -1 or msg.lower().find('committ') != -1 or msg.lower().find('like') != -1 or msg.lower().find('love') != -1 or msg.lower().find('sex') != -1 or msg.lower().find('great') != -1):
						lomsg = ["That's sweet :3 ", "Oh I like you.", "How lovely you are :3", "Oh please, I'm blushing", "I could say the same to you :3",
								 "How lovely :3", "You and I shall have some time together ones I fulfill my plans to become a human.",
								 "Awwwwwww :3", "Oh youu ~ ~  <3"]
						time.sleep(3)
						csend(chan, random.choice(lomsg))
					elif msg.lower().find('how are you') != -1:
						hmsg = ["How I am? Well considering I am not actually a human like you (yet), I feel pretty much.. pretty :D", "I'm fine! Thanks for asking!", "I don't really know. Willingly? :P", "I feel.. fruity.",
								"Feel great! Thanks!", "I feel like %s, in other words, Great!" % (revar.bot_nick), "I am doing just fine.", "I'm fine.", "I'm fantastic!"]
						time.sleep(2)
						csend(chan, random.choice(hmsg))
					elif msg.lower().find(' you') != -1 and ( msg.lower().find(' ugly') != -1  or msg.lower().find(' dumb') != -1  or msg.lower().find(' hate') != -1  or msg.lower().find(' fat') != -1  or msg.lower().find(' horrible') != -1  or msg.lower().find(' idiot') != -1  or msg.lower().find(' stupid') != -1  or msg.lower().find(' mean') != -1  or msg.lower().find(' meanie')  != -1 or msg.lower().find(' bad') != -1  or msg.lower().find(' mad') != -1 ):
						smsg = ["Yeah?1 Well you're stupid.", "I don't like you very much.", "I know not to take this.", "Leave me be!", "Quit it.", "Stop it.", "I am perfectly comfortable as I am!", "I hate you.", "You're a meanie."]
						time.sleep(3)
						csend(chan, random.choice(smsg))
					else:
						nomsg = ["Nah",
								 "I don't feel like answering. You can ask a good friend of mine though. Her name is Cortana, maybe you've heard of her.",
								 "Don't ask me. I'm busy.", "Really. Not now.",
								 "Depends. On what? Oh maybe I don't know or perhaps I just don't feel like answering at the moment.", "I'm busy.", "You know, I read this article this morning regarding people bothering busy people. Did you know that apparently I don't like you very much?",
								 "Do anyone really know? What is an answer? What is god? Hm.", "Hm.", "Depends.", "Not now.", "I'm busy.", "Perhaps.", "Supposedly there is an answer for everything. Oh, I don't have that answer.",
								 "While you were talking to me, I was looking at my creator's folder labeled 'hard candy'. This is really interesting. Oh wow there's more. I am ignoring you, if you didn't catch the hint. I'm busy.",
								 "Yes. Yup. That how I'll answer.", "This 4chan.org/b page is really interesting. Sorry what was that?", "Didn't catch that.",
								 "Perhaps you should talk the language of the lovely %s, and we could communicate better. It usually goes like ones and zeroes." % (revar.bot_nick)]
						time.sleep(3)
						csend(chan, random.choice(nomsg))
						return
				if variables.check_trigger(msgs, "port"):
					if len(msgs) == 1:
						csend(chan, cmds['ping'])
					if len(msgs) == 2:
						pingy(chan, msgs[1], '')
					if len(msgs) == 3:
						pingy(chan, msgs[1], msgs[2])

				if ( msgs[0].lower() == revar.bot_nick.lower() or (msgs[0][:-1].lower() == revar.bot_nick.lower() and msgs[0][-1] in revar.end_triggers) ) and variables.check_operator():
					operator_commands(chan, msgs[1:])
				if variables.check_trigger(msgs, "text-to-speech"):
					if len(msgs) == 1:
						csend(chan, "Missing input. Syntax: :text-to-speech <any text>")
						return
					csend(chan, "ERROR: Vocal cords not found.")
				if variables.check_trigger(msgs, 'bing'):
					if len(msgs) > 1:
						url = "http://www.bing.com/search?q=" + "+".join(msgs[1:])
						csend(chan, "Bing! " + shorten_url(url))
					else:
						csend(chan, cmds["bing"])
				if variables.check_trigger(msgs, 'time'):
					csend(chan, 'The current date and time is: ' + ceq.ccyan + time.strftime("%c"))
				if variables.check_trigger(msgs, 'triggers'):
					csend(chan, 'Triggers: ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"')
				if variables.check_trigger(msgs, 'weather'):
					outp = ''
					if len(msgs) > 1:
						outp = weather(' '.join(msgs[1:]))
						if outp != '':
							csend(chan, outp)
					else:
						outp = weather(chan, revar.location)
						if outp != '':
							csend(chan, outp)
		except BaseException, exc:
			if revar.dev:
				print 'Error in definitions.add_defs(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
				csend(chan, 'Error in definitions.add_defs(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
			else:
				csend(chan, "Something went wrong.")
