# -*- coding: utf-8 -*-
__author__ = 'Johan Hoiness'

import connection
import config
import revar
import ceq
import sys
import time

version = "1.0." + connection.commit
ftime = ''
s = connection.s
mute = False
google_api = "AIzaSyDkxx5jT2ZWsLZH6vQ_PctkqLngUarvfbc"
personalityforge_api = "QIS4aOi74xGngkn1"
last_pong = time.time()


def check_operator(user):
	operators = revar.operators
	operatorlist = ['']
	for item in operators:
		operatorlist.append(item.lower())
	if user.lower() in operatorlist:
		return True
	else:
		return False


def get_exc(exc, errormsgdev, errormsg=''):
	if revar.dev:
		print 'Failed, line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
		return "Error in "+errormsgdev+", line " + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
	else:
		return "Something went wrong{}.".format(errormsg)


def checkrec(chan, user, msg):
	msgs = msg.split()
	line = msg
	pm = False
	notice = False
	rec = ''
	if revar.outputredir:
		if len(line) > 1 and (' '.join(line).find('<') != -1 or ' '.join(line).find('>') != -1):
			if not revar.outputredir_all:
				if not check_operator(user):
					return
			if line[-1] == '<':
				msg = msg.split()
				msg = ' '.join(msg[:-1])
				msgs = msgs[:-1]
				line = line[:-1]
				rec = user
				pm = True
			if line[-1] == '<<':
				msg = msg.split()
				msg = ' '.join(msg[:-1])
				msgs = msgs[:-1]
				line = line[:-1]
				rec = user
				notice = True
			if len(line) > 2:
				if line[-2] == '>':
					msg = msg.split()
					msg = ' '.join(msg[:-2])
					msgs = msgs[:-2]
					line = line[:-2]
					rec = line[-1]
					pm = True
				if line[-2] == '>>':
					msg = msg.split()
					msg = ' '.join(msg[:-2])
					msgs = msgs[:-2]
					line = line[:-2]
					rec = line[-1]
					notice = True
	return msg, rec, notice, pm


def ssend(msg):
	if msg == '':
		return False
	if config.verbose == True:
		print ftime + ' >> ' + msg
	connection.s.send(msg + '\n')


def csend(chan, msg, notice=False, pm=False, rec=''):
	if not mute:
		if chan == '' or msg == '':
			return False
		if msg.find('&DEGREE;') != -1:
			msg = msg.replace('&DEGREE;', '°')

		over = ''
		text = ''
		if len(msg) > 428:
			over = msg[425:]
			msg = msg[:425]
		else:
			over = ''

		if notice:
			if config.verbose:
				print ftime + ' >> ' + 'NOTICE %s :%s' % (chan, msg)
			else:
				print ftime + ' >> NOTICE %s: %s' % (chan, msg)
			s.send('NOTICE %s :%s%s' % (rec, ceq.hiddenc.encode('utf-8'), msg) + '\n')
		if pm == True:
			if config.verbose == True:
				print ftime + ' >> ' + 'PRIVMSG %s :%s' % (chan, msg)
			else:
				print ftime + ' >> PM %s: %s' % (chan, msg)
			s.send('PRIVMSG %s :%s%s' % (rec, ceq.hiddenc.encode('utf-8'), msg) + '\n')
		if config.verbose == True:
			print ftime + ' >> ' + 'PRIVMSG %s :%s' % (chan, msg)
		else:
			print ftime + ' >> %s: %s' % (chan, msg)
		s.send('PRIVMSG %s :%s%s' % (chan, ceq.hiddenc.encode('utf-8'), msg) + '\n')
		if over != '':
			csend(chan, over)


def check_midsentencecomment(msg):
	if revar.midsentence_comment:
		if msg.lower().find("\\") != -1:
			msg = msg[:msg.find("\\")]
			return msg
	return msg


def check_midsentencetrigger(msg):
	if revar.midsentence_trigger:
		if msg.lower().find(" :(") != -1 and msg.lower().find(')') != -1:
			msg = msg[msg.find(' :('):msg.find(')')].replace(' :(', revar.triggers[0])
			return msg
	return msg


def check_triggers(msg):
	for trigger in revar.triggers:
		triggert = '|S|' + trigger.lower()
		msgt = '|S|' + msg.lower()
		if msgt.find(triggert) != -1:
			msg = msg[len(trigger):]
			return msg
	return False


def check_bottriggers(msg):
	for trigger in revar.end_triggers:
		msgt = '|S|'+msg.lower()
		findtext = '|S|'+revar.bot_nick.lower()+trigger.lower()+' '
		if msgt.find(findtext) != -1:
			msg = msg[len(findtext)-3:]
			return msg
	return False


def getexc(exc, filen):
	if revar.dev:
		return 'Error in {}, line '.format(filen) + str(sys.exc_info()[2].tb_lineno) + ': ' + str(exc)
	else:
		return 'Error in {}.'.format(filen)