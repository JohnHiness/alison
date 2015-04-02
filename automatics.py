__author__ = 'Johan Hoiness'

import sys
import general
import revar
from time import strftime
import time
import config
import commands


def get_ftime():
	if config.verbose:
		print 'automatics.get_ftime() started.'
	while True:
		general.ftime = '[' + strftime('%H:%M:%S') + ']'
		time.sleep(1)


def autoping():
	if config.verbose:
		print 'automatics.autoping() started.'
	autoping = time.time()
	while True:
		if time.time() - autoping > 60:
			general.ssend('PING DoNotTimeoutMePlz')
			general.ssend("TIME")
			general.ssend("WHOIS " + revar.bot_nick.lower())
			autoping = time.time()
		time.sleep(1)


def autoweather():
	if config.verbose:
		print 'automatics.autoweather() started.'
	autoweather_last = time.time() - 90
	while True:
		if revar.autoweather and time.time() - autoweather_last > 90 and int(strftime('%H%M')) == revar.autoweather_time:
			autoweather_last = time.time()
			outp = ''
			outp = commands.weather(revar.location)
			if outp != '':
				general.csend(','.join(revar.channels), outp)
		time.sleep(1)


def checkpongs():
	if config.verbose:
		print 'automatics.checkpongs() started.'
	while True:
		print time.time() - general.last_pong
		if time.time() - general.last_pong > 200:
			print 'Connection timeout to server.'
			sys.exit(0)
		time.sleep(2)