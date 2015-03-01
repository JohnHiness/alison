#!/usr/bin/python
import socket
import sys
import random
import time
from datetime import datetime
import config

version = "0.61"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
leave_messages = ["I will be blac.. cough cough ..back. I'll be back.", "SOMEONES HACKING! I'M OFF TO BATTLE!", "I can fix everything. I have duct tape.", "Can't think of a joke. Ask Cortana.", "Pooooooooofffffff i'm outta here..", "I generally avoid temptation.. unless I can't resist it"]
localtime = time.localtime(time.time())
ftime = "[%s:%s:%s]" % (datetime.now().hour, datetime.now().minute, datetime.now().second)
raw_text = ''
rawer_text = ''
user = raw_text[1:raw_text.find('!')]
msg = raw_text[raw_text.find(':'):500][1:500]
msg = msg[msg.find(':'):500][1:500].replace('\n', '').replace('\r', '')

def ssend(text):
        print ftime + ' >> ' + text
        s.send(text + '\n')
def csend(text):
        print ftime + ' >> %s: %s' % (config.channel, text)
        s.send('PRIVMSG %s :%s\n' % (config.channel, text))
def psend(user, text):
        print ftime + ' >> %s: %s' % (user, text)
        s.send("PRIVMSG %s :%s\n" % (user, text))

