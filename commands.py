__author__ = 'Johan Hoiness'


import revar
import general
import json
import urllib2
import ceq
import config
import os
import socket
import time
import connection
import sys
import thread
import urllib
from datetime import datetime

b = ceq.cbold
r = ceq.creset
cyan = ceq.ccyan
violet = ceq.cviolet
orange = ceq.corange


def shorten_url(url):
	try:
		post_url = 'https://www.googleapis.com/urlshortener/v1/url?&key=' + general.google_api
		postdata = {'longUrl':url,
					'key':general.google_api}
		headers = {'Content-Type':'application/json'}
		req = urllib2.Request(
			post_url,
			json.dumps(postdata),
			headers
		)
		ret = urllib2.urlopen(req).read()
		return json.loads(ret)['id']
	except BaseException as exc:
		return general.get_exc(exc, 'commands.shorten_url()')


def get_hash(imdb_id):
	try:
		torrent_hash = ''
		if not revar.get_hash:
			return
		url3 = "https://yts.to/api/v2/list_movies.json?query_term=" + imdb_id
		data3 = json.load(urllib2.urlopen(url3, timeout=8))
		quality1080 = ''
		quality720 = ''
		if data3['data']['movie_count'] == 0:
			return ''
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
		return xhash
	except BaseException as exc:
		return general.get_exc(exc, 'commands.get_hash()')


def imdb_info(kind, simdb):
	if kind == 'id':
		url = "http://www.omdbapi.com/?i=" + simdb + "&plot=short&r=json"
	elif kind == 'search':
		params = {
			"q": ' '.join(simdb),
		}
		url2 = "http://www.imdb.com/xml/find?json=1&" + urllib.urlencode(params)
		print url2
		try:
			data2 = json.load(urllib2.urlopen(url2, timeout=8))
			try:
				if len(data2["title_popular"]) < 1:
					return "Title not found11."
				imdbID = data2["title_popular"][0]["id"]
			except:
				try:
					if len(data2["title_exact"]) < 1:
						return "Title not found."
					imdbID = data2["title_exact"][0]["id"]
				except:
					return "Title not found."
			url = "http://www.omdbapi.com/?i=" + imdbID
		except:
			url = "http://www.omdbapi.com/?t=" + '+'.join(simdb)
	else:
		print 'Wrong function parameters: %s %s' % (kind, simdb)
	print 'Getting IMDB-info with url: ' + url
	try:
		data = json.load(urllib2.urlopen(url, timeout=12))
	except urllib2.URLError, e:
		if revar.dev:
			return "API returned with error: %r" % e
		else:
			return "Something went wrong requesting information."
	except BaseException as exc:
		return general.get_exc(exc, 'imdb_info()')
	if data['Response'].lower() == 'false':
		if data['Error'] == 'Movie not found!':
			return 'Title not found.'
		else:
			return data['Error']

	try:
		print data
		i_id = data['imdbID']
		i_link = shorten_url('http://imdb.com/title/' + i_id)[7:]
		torrent_hash = get_hash(data['imdbID'])
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
		return general.get_exc(exc, 'commands.imdb_info()-get-info')
	if torrent_hash.find(',') != -1:
		return torrent_hash
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
	if torrent_hash != '':
		si_magnet = ' ' + b + '|' + b + ' YIFY-Torrent: %s' % shorten_url('https://yts.to/torrent/download/' + torrent_hash + '.torrent').replace('http://', '')
	else:
		si_magnet = ''
	send_text = si_type + ceq.corange + b + si_title + r + ceq.cblue + si_year + r + violet + si_runtime + si_imdbrating + si_metarating + si_genre + ceq.cred + si_link + si_magnet + r + si_plot
	if len(send_text) > 424:
		send_text = send_text[0:421] + '...'
	return send_text.encode('utf-8')


def save_revar(chan):
	try:
		dict_of_var = {
			'midsentence_comment':revar.midsentence_comment, 'midsentence_trigger':revar.midsentence_trigger, 'outputredir_all':revar.outputredir_all, 'outputredir':revar.outputredir, 'ignorelist':revar.ignorelist, 'whitelist':revar.whitelist, 'ignorelist_set':revar.ignorelist_set, 'whitelist_set':revar.whitelist_set, 'end_triggers':revar.end_triggers, 'triggers':revar.triggers, 'get_hash':revar.get_hash, 'bot_nick':"\""+revar.bot_nick+"\"", 'operators':revar.operators, "channels":revar.channels, "dev":revar.dev, "location":"\""+revar.location+"\"", "autoweather":revar.autoweather, "autoweather_time":revar.autoweather_time, "weather_custom":revar.weather_custom, "chatbotid":revar.chatbotid,
		}
		#os.rename( "revar.py", "revar.bak" )
		with open( "revar.py", "w" ) as target:
			for variable_name in dict_of_var:
				target.write("{0} = {1}\n".format(variable_name, dict_of_var[variable_name]))
			target.close()
		return True
	except BaseException as exc:
		if revar.dev:
			pass
			#print 'Failed to save to file, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
			#csend(chan, "Error in when trying to rewrite revar.py, line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
		else:
			pass
			# csend(chan, "Something went wrong trying to save.")
		return False


def refresh_version(chan):
	try:
		url7 = "https://api.github.com/repos/johanhoiness/alison/commits"
		data7 = json.load(urllib2.urlopen(url7, timeout=8))
		if data7[0]['commit']['url'][data7[0]['commit']['url'].find('commits/') + 8 :][:7] != '':
			connection.commit = data7[0]['commit']['url'][data7[0]['commit']['url'].find('commits/') + 8 :][:7]
		else:
			return False
		with open( "connection.py", "w" ) as target:
			target.write("import socket\ns = socket.socket( )\ncommit = '{}'".format(connection.commit))
			target.close()
			return True
	except BaseException, exc:
		if revar.dev:
			print 'Failed to save to file, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
			general.csend(chan, "Error in when trying to rewrite connection.py, line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc))
		else:
			general.csend(chan, "Something went wrong trying to save.")
		return False


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


def operator_commands(chan, msgs):
	try:
		if not msgs:
			return ''
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
			"{0:s}chatbotid({1:s}int={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, str(revar.chatbotid)),
		#   "{0:s}variable({1:s}string={2:s}{3:s}{0:s})".format(ceq.ccyan, ceq.cblue, ceq.cviolet, ),
		]
		if (len(msgs) > 1) and msgs[0].lower() == 'ignore':
			revar.ignorelist.append(msgs[1])
			return 'Ignoring user %s.' % msgs[1]
		if msgs[0].lower() == 'mute':
			general.mute = True
		if msgs[0].lower() == 'umute' or msgs[0].lower() == 'unmute':
			general.mute = False
		if (len(msgs) == 2) and msgs[0].lower() == 'unignore':
			try:
				revar.ignorelist.remove(msgs[1])
				return "No longer ignoring user '%s'" % msgs[1]
			except:
				return "Ignored user was not found. Make sure you typed it in correctly."
		if (len(msgs) > 1) and (msgs[0].lower() == 'whitelist' or msgs[0].lower() == 'white'):
			revar.whitelist.append(msgs[1])
			return 'User %s is now whitelisted' % msgs[1]
		if (len(msgs) == 2) and (msgs[0].lower() == 'unwhitelist' or msgs[0].lower() == 'un;white' or msgs[0].lower() == 'niggerfy'):
			try:
				revar.whitelist.remove(msgs[1])
				return "User '%s' no longer whitelisted" % msgs[1]
			except:
				return "Whitelisted user was not found. Make sure you typed it in correctly."
		if len(msgs) > 0 and msgs[0].lower() == 'config':
			if len(msgs) > 1:
				if msgs[1].lower() == 'set':
					if len(msgs) == 2:
						return ceq.cred + "Variables: " + ', '.join(variable_list)
					if msgs[2].lower() == 'triggers':
						if len(msgs) > 3:
							revar.triggers = (' '.join(msgs[3:]).replace(', ', '||')).lower().replace('"', '').replace('$botnick', revar.bot_nick.lower()).split('||')
							print (' '.join(msgs[3:]).replace(', ', '||'))
							print revar.triggers
							return 'New triggers: ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"'
						else:
							return 'Current triggers(use same format when setting): ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"'
					if msgs[2].lower() == 'location':
						if len(msgs) > 3:
							revar.location = ' '.join(msgs[3:])
							return 'New location: ' + ceq.cred + revar.location
						else:
							return 'Current location: ' + ceq.cred + revar.location
					if msgs[2].lower() == 'ignorelist' or msgs[2].lower() == 'ignore':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.ignorelist_set = True
								return 'Ignorelist set to True. I will now ignore any users on that list.'
							elif msgs[3].lower() == 'false':
								revar.ignorelist_set = False
								return 'Ignorelist set to False. I will no longer ignore any users that are on the ignorelist.'
							else:
								return 'Use "true" or "false".'
						else:
							'Enable or disable the ignore-feature. Default is Off. Use "config set ignorelist <true|false>" to set.'
					if msgs[2].lower() == 'whitelist' or msgs[2].lower() == 'white':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.whitelist_set = True
								return 'Whitelist set to True. I will now ignore any users NOT on that list.'
							elif msgs[3].lower() == 'false':
								revar.whitelist_set = False
								return 'Whitelist set to False. I will no longer ignore any users that aren\'t on the whitelist.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable the whitelist-feature. Default is Off. Use "config set whitelist <true|false>" to set.'
					if msgs[2].lower() == 'commentchar' or msgs[2].lower() == 'comment':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.midsentence_comment = True
								return 'Midsentence_comment set to True.'
							elif msgs[3].lower() == 'false':
								revar.midsentence_comment = False
								return 'Midsentence_comment set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable the midsentence-commentout-feature. Default is Onn. Use "config set commentchar <true|false>" to set.'
					if msgs[2].lower() == 'weather_custom':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.weather_custom = True
								return 'Weather_custom set to True.'
							elif msgs[3].lower() == 'false':
								revar.weather_custom = False
								return 'Weather_custom set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable custom weather descriptions.'

					if msgs[2].lower() == 'commentchar' or msgs[2].lower() == 'comment':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.midsentence_comment = True
								return 'Midsentence_comment set to True.'
							elif msgs[3].lower() == 'false':
								revar.midsentence_comment = False
								return 'Midsentence_comment set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable the midsentence-commentout-feature. Default is Onn. Use "config set commentchar <true|false>" to set.'

					if msgs[2].lower() == 'chatbotid':
						if len(msgs) > 3:
							if not msgs[3].isdigit():
								return 'Variable is an interger. Use only numbers.'
							revar.chatbotid = int(msgs[3])
							return 'Chatbotid is set to ' + str(revar.chatbotid)
						else:
							return "Change the ChatBotID from PersonalityForge. To see a list of available ID's, go to http://personalityforge.com Make sure the new ChatBot is made 'Run Free' by the creator."

					if msgs[2].lower() == 'dev':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.dev = True
								return 'Dev set to True.'
							elif msgs[3].lower() == 'false':
								revar.dev = False
								return 'Dev set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable certain failsafes, making the bot less stabel but outputs better error-messages. Default is False. Use "config set dev <true|false>" to set.'
					if msgs[2].lower() == 'midsentence_trigger' or msgs[2].lower() == 'midtrigger':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.midsentence_trigger = True
								return 'Midsentence_trigger set to True.'
							elif msgs[3].lower() == 'false':
								revar.midsentence_trigger = False
								return 'Midsentence_trigger set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable the midsentence-trigger-feature. Type ":(<command>)" in any part of the message to trigger commands. Default is Off. Use "config set commentchar <true|false>" to set.'
					if msgs[2].lower() == 'autoweather' or msgs[2].lower() == 'autoweather':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.autoweather = True
								return 'Autoweather set to True.'
							elif msgs[3].lower() == 'false':
								revar.autoweather = False
								return 'Autoweather set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable the automatic forecast.'
					if msgs[2].lower() == 'get_hash':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.get_hash = True
								return 'Get_hash set to True.'
							elif msgs[3].lower() == 'false':
								revar.get_hash = False
								return 'Get_hash set to False.'
							else:
								return 'Use "true" or "false".'
						else:
							return 'Enable or disable IMDB from trying to get hash/torrents (quickens response time). Default is True. Use "config set get_char <true|false>" to set.'
					if msgs[2].lower() == 'autoweather_time':
						if len(msgs) > 3:
							if not msgs[3].isdigit():
								return 'Variable must be numbers only'
							if not len(msgs[3]) == 4:
								return 'You must use 4 digits for this variable.'
							revar.autoweather_time = int(msgs[3])
							return 'New autoweather_time: ' + str(revar.autoweather_time)
						else:
							return 'Change what time the autoweather should trigger. Format is digits only, as HHSS.'

					if msgs[2].lower() == 'point-output' or msgs[2].lower() == 'outputredir':
						if len(msgs) > 3:
							if msgs[3].lower() == 'true':
								revar.outputredir = True
								return 'Point-output set to On.'
							elif msgs[3].lower() == 'false':
								revar.outputredir = False
								return 'Point-output set to Off.'
							elif msgs[3].lower() == 'all':
								revar.outputredir_all = True
								return 'Point-output set to available for all.'
							elif msgs[3].lower() == 'ops' or msgs[3].lower() == 'op':
								revar.outputredir_all = False
								return 'Point-output set to available only for operators.'
							else:
								return 'Use "true", "all", "ops" or "false".'
						else:
							return 'Enable or disable the point-output feature. See "help point-output". Default is True, for only ops. Use "config set point-output <all|ops|true|false>" to set.'
				if msgs[1].lower() == 'save':
					if save_revar(chan):
						return "Configurations successfully saved to file."
			else:
				return 'Here you can edit configurations and other variables of the bot. From here you can either "set" or "save". By setting you are changing the current bot, and by saving you are changing files of the bot - making the configuration permanent.'

		if len(msgs) > 0 and msgs[0].lower() == 'op':
			if len(msgs) > 1:
				revar.operators.append(msgs[1].lower())
				return "User '%s' is now an operator." % msgs[1]
			else:
				return 'Usage: "op <nick>".'
		if len(msgs) > 0 and msgs[0].lower() == 'nick':
			general.ssend("NICK " + msgs[1])
			general.ssend("TIME")
			revar.bot_nick = msgs[1]
		if msgs[0].lower() == 'quit':
			general.csend(','.join(revar.channels), "I'm off!")
			general.ssend('QUIT ' + config.leave_message)
			thread.interrupt_main()
		if msgs[0].lower() == 'join':
			if len(msgs) < 2:
				return 'No channel specified.'
			revar.channels.append(msgs[1].lower())
			general.ssend('JOIN {}'.format(msgs[1].lower()))
			general.ssend('TIME')
			general.ssend('WHOIS {}'.format(revar.bot_nick.lower()))
			return 'Joined {}.'.format(msgs[1])
		if msgs[0].lower() == 'part':
			if len(msgs) > 1:
				chan_to_leave = msgs[1].lower()
			else:
				chan_to_leave = chan
			if chan_to_leave not in revar.channels:
				return "I'm not in that channel."
			general.ssend('PART {}'.format(chan_to_leave))
			revar.channels.remove(chan_to_leave)
			return 'Parted with {}.'.format(chan_to_leave)
		if msgs[0].lower() == 'restart':
			general.csend(chan, 'Restarting..')
			general.ssend('QUIT ' + config.leave_message)
			python = sys.executable
			print str(python)+'||'+str(python)+'||'+ str(* sys.argv)
			os.execl(python, python, * sys.argv)
		if msgs[0].lower() == 'git-update':
			print 'Pulling from Git and updating...'
			try:
				url4 = "https://api.github.com/repos/johanhoiness/alison/commits"
				data4 = json.load(urllib2.urlopen(url4, timeout=4))
				general.csend(chan, ceq.ccyan + 'Last commit: ' + ceq.cviolet + data4[0]['commit']['message'].encode('utf-8'))
			except:
				print 'Failed to get commit-message from git.'
			try:
				outp = os.system("git pull http://github.com/johanhoiness/alison")
				if outp != 0:
					return "Update failed."
				outp2 = os.system("python -O -m py_compile alison.py connection.py ceq.py config.py revar.py commands.py general.py automatics.py")
				if outp2 != 0:
					return "Download was successful but the compilation failed."
				if not refresh_version(chan):
					return 'Something went wrong updating local committ-id.'
				general.ssend('QUIT ' + config.leave_message)
				python = sys.executable
				print str(python)+'||'+str(python)+'||'+ str(* sys.argv)
				os.execl(python, python, * sys.argv)
				return 'Done'
			except:
				return 'Download or installation failed.'
		if len(msgs) > 0 and msgs[0].lower() == 'deop':
			if len(msgs) > 1:
				try:
					revar.operators.remove(msgs[1].lower())
					return "User '%s' is no longer an operator." % msgs[1]
				except:
					return "Operator not found. Make sure you typed it in correctly."
			else:
				return 'Usage: "deop <nick>".'
		if len(msgs) > 0 and msgs[0].lower() == 'help':
			if len(msgs) > 1:
				try:
					return operator_cmds[msgs[1].lower()]
				except:
					return "Command or function not found. Make sure you typed it in correctly."
			else:
				retrn = "This help is for operator- commands and functions. There are currently %d of them. To use any of them, they must start by saying \"%s\" first, and can only be accessed by operators. To get more information on the command/function, use \"help <command>\"." % (len(operator_cmds), revar.bot_nick) + '\n'
				return retrn + "These are the ones available: " + ', '.join(operator_cmds.keys())
		if len(msgs) > 0 and msgs[0] == 'save':
			return "All configurations can be saved by using \"config save\"."
		if len(msgs) == 0:
			return "All commands launched this way is for operators only. It is only to edit settings and variables. See \"%s: help\" for more information." % revar.bot_nick
	except BaseException as exc:
		if revar.dev:
			print 'Error in definitions.operator_commands(), line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
			return "Error in definitions.operator_commands(), line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
		else:
			return "Something went wrong processing operator command."

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


def weather(location=revar.location.split()):
	try:
		url5 = "http://api.openweathermap.org/data/2.5/weather?q={0}&mode=json".format(str('+'.join(location)))
		data5 = json.load(urllib2.urlopen(url5, timeout=8))
		if config.verbose:
			print data5
		if data5['cod'] == '404':
			return "Location not found."
		if data5['cod'] != 200:
			return 'Error in request.'
		if revar.weather_custom and data5['weather'][0]['id'] in weather_codes.keys():
			w_desc = weather_codes[data5['weather'][0]['id']]
		else:
			w_desc = data5['weather'][0]['description']
		w_temp = data5['main']['temp'] - 273.15
		w_country = data5['sys']['country']
		w_wind = data5['wind']['speed']
		if w_country == '':
			return "Location not found."
		w_city = data5['name']
		text_to_send = "{0}Current weather of {3}{4}{0}, {1}{2}{0}: {11}{6}{0}, {10}with a temperature of {7}{8}&DEGREE;{10} celsius and a windspeed of {7}{9}{10} m/s.".format(ceq.cblue, ceq.cred, w_country.encode('utf-8'), ceq.cviolet, w_city.encode('utf-8'), ceq.ccyan, w_desc, ceq.corange, w_temp, w_wind, ceq.clcyan, ceq.cgreen, ceq.degree)
		return text_to_send.decode('utf-8').encode('utf-8')
	except BaseException as exc:
		return general.get_exc(exc, 'commands.weather()')


def forecast(location=revar.location.split()):
	try:
		url5 = "http://api.openweathermap.org/data/2.5/forecast?q={}&mode=json&cnt=9".format(str('+'.join(location)))
		data6 = json.load(urllib2.urlopen(url5, timeout=8))
		if config.verbose:
			print data6
		if data6['cod'] == '404':
			return "Location not found."
		if data6['cod'] != '200':
			return 'Error in request.'
		nowt = datetime.now()
		seconds_since_midnight = int((nowt - nowt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
		seconds_to = (24 * 3600) - seconds_since_midnight
		epoch_to_mid = int(time.time()) + seconds_to
		next_0900NO = epoch_to_mid + 2*3600 + 12*3600
		new_data6 = ''
		for listdt in data6['list']:
			if listdt['dt'] == next_0900NO:
				print listdt
				new_data6 = listdt
		if not new_data6:
			return 'Next-days time not found in API-response.'
		data7 = new_data6
		if revar.weather_custom and data7['weather'][0]['id'] in weather_codes.keys():
			w_desc = weather_codes[data7['weather'][0]['id']]
		else:
			w_desc = data7['weather'][0]['description']
		w_temp = data7['main']['temp'] - 273.15
		w_country = data6['city']['country']
		w_wind = data7['wind']['speed']
		if w_country == '':
			return "Location not found."
		w_city = data6['city']['name']
		text_to_send = "{0}Forecast of {3}{4}{0}, {1}{2}{0}, for tomorrow midday: {11}{6}{0}, {10}with a temperature of {7}{8}&DEGREE;{10} celsius and a windspeed of {7}{9}{10} m/s.".format(ceq.cblue, ceq.cred, w_country.encode('utf-8'), ceq.cviolet, w_city.encode('utf-8'), ceq.ccyan, w_desc, ceq.corange, w_temp, w_wind, ceq.clcyan, ceq.cgreen, ceq.degree)
		return text_to_send.decode('utf-8').encode('utf-8')
	except BaseException as exc:
		return general.get_exc(exc, 'commands.forecast()')


def porty(flags):
	if len(flags) == 2:
		address = flags[0]
		if not flags[1].isdigit():
			return 'Port must be numbers only.'
		port = flags[1]
	elif len(flags) == 1:
		address = flags[0]
		port = ''
	else:
		return 'Usage: port <address> <portnumber>  If no port is specified, I will only check if I can get a response from the network.'
	if port == '':
		response = os.system("ping -c 1 -W 8 " + address)
		if response == 0:
			return address + ' is up!'
		else:
			return address + ' is down!'
	else:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)
		result = sock.connect_ex((address,int(port)))
		if result == 0:
			return "Port %d on %s is open." % (int(port), address)
		else:
			return "Port %d on %s is closed or not responding." % (int(port), address)


def c_bing(msgs):
	if len(msgs) == 0:
		return
	return 'BING! ' + shorten_url('http://www.bing.com/search?q=' + '+'.join(msgs))


def c_imdb(msgs):
	return imdb_info('search', msgs)


def c_list(msgs):
	if len(msgs) > 0:
		if msgs[0].lower() == 'operators' or msgs[0].lower() == 'op' or msgs[0].lower() == 'admin':
			if revar.operators == '':
				return 'There are no operators listed.'
			else:
				return 'Operator(s): ' + ceq.cred + ', '.join(revar.operators)
		elif msgs[0].lower() == 'ignore' or msgs[0].lower() == 'ignored' or msgs[0].lower() == 'ignorelist':
			if revar.ignorelist == []:
				return 'There are no ignored users.'
			else:
				return 'Ignored users: ' + ', '.join(revar.ignorelist)
		elif msgs[0].lower() == 'whitelist' or msgs[0].lower() == 'white' or msgs[0].lower() == 'whites':
			if revar.whitelist == []:
				return 'There are no users being whitelisted.'
			else:
				return 'Whitelisted users: ' + ', '.join(revar.whitelist)
		elif msgs[0].lower() == 'channels' or msgs[0].lower() == 'chan':
			return '{}Channels I am currently in: {}{}'.format(ceq.cgreen, ceq.cred, '{}, {}'.format(ceq.ccyan, ceq.cred).join(revar.channels))
		else:
			return "I can't find anything on that. Make sure you typed it right."
	else:
		return "You can use this ':list'-feature to get me to list the users that are operators(list op), channels(list <chan | channels>), ignored(list ignore), or whitelisted(list whitelist)."


def c_triggers():
	return 'Triggers: ' + ceq.ccyan + '"' + ceq.cred + ('%s", "%s' % (ceq.ccyan, ceq.cred)).join(revar.triggers) + ceq.ccyan + '"'


def c_say(text):
	return ' '.join(text)


def c_time():
	return 'The current date and time is: ' + ceq.ccyan + time.strftime("%c")


def c_version():
	return 'Running Alison v%s' % general.version


def personalityforge(usr, msg):
	try:
		params = {
			"apiKey": general.personalityforge_api,
			"chatBotID": revar.chatbotid,
			"message": msg,
			"externalID": "AlisonID" + usr,
			"firstName": usr
		}
		url = "http://www.personalityforge.com/api/chat/?" + urllib.urlencode(params)
		data = urllib2.urlopen(url, timeout=8).read()
		data = data[data.rfind('<br>')+4:]
		data = json.loads(data)
		print data
		if data['success'] == 0:
			return data['errorMessage']
		message = data['message']['message']
		for name in data['message']['chatBotName'].split():
			message = message.replace(name, revar.bot_nick)
		message = message.replace("{0} {0}".format(revar.bot_nick), revar.bot_nick)
		return "{}: {}".format(usr, message)

	except BaseException as exc:
		return general.getexc(exc, 'personalityforge')


def c_countdown(chan, flags):
	if chan in general.countdown:
		return 'Only one countdown allowed per channel. Stop the current countdown'
	if not flags:
		return 'You need to specify a number between 1 and 20.'
	if not flags[0].isdigit():
		return 'Must be numbers only, between 1 and 20.'
	if int(flags[0]) > 20:
		return 'Number cannot be higher than 20.'
	if int(flags[0]) < 1:
		return 'Number cannot be lower than 1.'
	general.countdown.append(chan)
	number = int(flags[0])
	while number != 0:
		if chan not in general.countdown:
			general.csend(chan, 'Countdown stopped.')
			return
		general.csend(chan, '{}...'.format(number))
		number -= 1
		time.sleep(1)
	general.csend(chan, 'GO!')
	general.countdown.remove(chan)
	return


def c_last_seen(flags):
	if not flags:
		return 'You must specify a user you want to know of said users last occurrence.'
	user = flags[0]
	if user.lower() not in general.last_seen.keys():
		return "User hasn't been registered. Meaning the user hasn't said anything since {}.".format(general.start_time)
	user = general.last_seen[user.lower()]
	sec = int(time.time() - user['time'])
	if sec < 60:
		if sec == 1:
			last_time = str(sec) + ' second ago'
		else:
			last_time = str(sec) + ' seconds ago'
	if sec >= 60:
		minutes = sec // 60
		if minutes == 1:
			last_time = str(minutes) + ' minute ago'
		else:
			last_time = str(minutes) + ' minutes ago'
	if sec >= 3600:
		hours = sec // 3600
		if hours == 1:
			last_time = str(hours) + ' hour ago'
		else:
			last_time = str(hours) + ' hours ago'
	if sec >= 86400:
		days = sec // 86400
		if days == 1:
			last_time = str(days) + ' day ago'
		else:
			last_time = str(days) + ' days ago'
	msg_to_retrn = "{4}{0} {7}was last seen {5}{1} {7}in channel {6}{2}{7}, with the message \"{8}{3}{7}\".".format(user['name'], last_time, user['channel'], user['message'], ceq.cviolet, ceq.cgreen, ceq.corange, ceq.cblue, ceq.ccyan)
	if len(msg_to_retrn) > 400:
		msg_to_retrn = msg_to_retrn[:400] + "... {}\".".format(ceq.cblue)
	return msg_to_retrn

cmds = {
	"imdb" : ceq.corange + "Syntax: " + ceq.cblue + "imdb <searchwords> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will search for movies or other titles from IMDB and will give you information on it. All links in the chat will automatecly be given information on too.",
	#"joke" : ceq.corange + "Syntax: " + ceq.cblue + "joke " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you a random joke!" ,
	#"test" : ceq.corange + "Syntax: " + ceq.cblue + "time " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you the time and the state of myself.",
	"point-output" : ceq.corange +"Syntax: " + ceq.cblue + "<any command> (< | << | > <user> | >> <user>) " + ceq.ccyan + "Description: " + ceq.cviolet + "I will direct the output of the command where the arrows are pointing. If they are pointing left, it will be directed to the one who called the command. Right, and it will go to the user written. Two arrows mean to send as Notice, one is to send as PM.",
	"help" : ceq.corange + "Syntax: " + ceq.cblue + "help <any command> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will tell you information on the things I can do with the command! If no command is spessified, I will list the available ones.",
	"say" : ceq.corange + "Syntax: " + ceq.cblue + "say <any text> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will say whatever you want me to say!",
	"list" : ceq.corange + "Syntax: " + ceq.cblue + "list <whitelist | ignore | op | operators> " + ceq.ccyan + "Description: " + ceq.cviolet + "I will list the users that are being ignored, whitelisted, or the operators.",
	"hey" : ceq.corange + "Syntax: " + ceq.cblue + "hey <text> " + ceq.ccyan + "Description: " + ceq.cviolet + "Send me a text and I will respond with a presonality! Remember that the only words I register, are the ones AFTER the 'hey'. The word 'hey' is not in the text I register.",
	"port" : ceq.corange + "Syntax: " + ceq.cblue + "port <address> <port> " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll check if the port is open on that network or not. If no port is given, I'll just see if the network is responding at all.",
	"bing" : ceq.corange + "Syntax: " + ceq.cblue + "bing <searchwords> " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll give you a link to the searchresults from the greatest search-engine of all time using your searchwords!",
	"time" : ceq.corange + "Syntax: " + ceq.cblue + "time " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll give you the full time! Oh and I won't allow you to give any parameters. Standardization, yo!",
	"weather" : ceq.corange + "Syntax: " + ceq.cblue + "weather <location| > " + ceq.ccyan + "Description: " + ceq.cviolet + "I'll tell you the weather and temperature of the given location. If no location is spesified, it will choose the default location which currently is set to %s." % revar.location,
	"operator-commands" : ceq.corange + "Syntax: " + ceq.cblue + "{0}<:|,| > <any operator-command>".format(revar.bot_nick) + ceq.ccyan + " Description: " + ceq.cviolet + "This is only accessable for operators. See \"$BOTNICK<:|,| > help\" for more information on this feature. All non-operators will be ignored calling a command this way.",
	"countdown": ceq.corange + "Syntax: " + ceq.cblue + "countdown <number of secconds>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will start a countdown with the specified number of seconds. The countown can be stopped by any user by typing 'stop' anywhere in chat. Only one countdown per channel is allowed.",
	"seen" : ceq.corange + "Syntax: " + ceq.cblue + "seen <user>" + '' + ceq.ccyan + " Description: " + ceq.cviolet + "Will tell you the last ocurence the user talked, with time, channel, and message. Note that this 'log' will be reset on startup.",
    "forecast" : ceq.corange + "Syntax: " + ceq.cblue + "forecast <location>" + ceq.ccyan + " Description: " + ceq.cviolet + "Will tell you the weather of the given location at the next midday. That is the next time the clock is 12:00. If no location is given, the default one will be used.",
	#"" : ceq.corange + "Syntax: " + ceq.cblue + "" + ceq.ccyan + " Description: " + ceq.cviolet + "",
}


def help_tree(msgs):
	if len(msgs) == 0:
		retrn = ceq.cblue + "These are the things you can tell me to do! You can say ':help <command>' and I'll tell you about the command you want information on." + '\n'
		return retrn + ceq.cblue + "There are {} of them, at the moment: ".format(len(cmds.keys())) + ceq.cviolet + '{1}, {0}'.format(ceq.cviolet, ceq.cred).join(cmds.keys())
	if len(msgs) > 0:
		try:
			return cmds[msgs[0].lower()]
		except:
			return "I can't find that one, sorry. Make sure you typed it in correctly."


def check_called(chan, user, msg):
	if not msg:
		return ''
	msgs = msg.split()
	if len(msgs) < 2:
		flags = []
	else:
		flags = msgs[1:]
	command = msgs[0].lower()
	if command == 'bing':
		return c_bing(flags)
	if command == 'imdb':
		return c_imdb(flags)
	if command == 'list':
		return c_list(flags)
	if command == 'weather':
		if not flags:
			return weather(revar.location.split())
		return weather(flags)
	if command == 'trigger' or command == 'triggers':
		return c_triggers()
	if command == 'port':
		return porty(flags)
	if command == 'say':
		return c_say(flags)
	if command == 'time':
		return c_time()
	if command == 'help':
		return help_tree(flags)
	if command == 'version':
		return c_version()
	if command == 'hey':
		return personalityforge(user, msg)
	if command == 'countdown' or command == 'count':
		return c_countdown(chan, flags)
	if command == 'last' or command == 'seen':
		return c_last_seen(flags)
	if command == 'forecast':
		if not flags:
			return forecast(revar.location.split())
		return forecast(flags)