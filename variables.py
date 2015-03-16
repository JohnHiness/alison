# -*- coding: utf-8 -*-
# !/usr/bin/python
import socket
import sys
import random
import time
import datetime
import config
import soconnect
import ceq
import lists
import definitions

version = "0.23.1"
end_triggers = [' ', '', ',', ':', '|']
triggers = [':', 'hax dis: ', '#sly ',]
def check_trigger(trigger):
	msgs = definitions.msgs
	if ('||START||' + ' '.join(msgs).lower() + ' ||END||')[9:('||START||' + ' '.join(msgs).lower() + ' ||END||').find(trigger.lower() + ' ')].lower() in triggers:
		definitions.msgs = (triggers[0] + ' '.join(msgs).lower()[(' '.join(msgs).lower().find(trigger.lower())):]).split()
		return True
	else:
		return False
s = soconnect.s
leave_messages = ["I will be blac.. cough cough ..back. I'll be back.", "SOMEONES HACKING! I'M OFF TO BATTLE!",
				  "I can fix everything. I have duct tape.", "Can't think of a joke. Ask Cortana.",
				  "Pooooooooofffffff i'm outta here..", "I generally avoid temptation.. unless I can't resist it"]
hva = ["Piteousness Of Doves", "A charm of finches", "Skein Of Goslings", "Army Of Caterpillars", "Herd Of Antelope",
	   "A mischief of mice", "Implausibility Of Gnus", "Cote Of Doves", "Bevy Of Deer (Roe Deer)", "Shrewdness Of Apes",
	   "A flange of baboons", "Flock Of Chickens", "Horde Of Gnats", "Down Of Hares", "Colony Of Badgers",
	   "Herd Of Elephants", "Flange Of Baboons", "Passel Of Hogs", "Tower Of Giraffes", "Charm Of Finches",
	   "A parliament of owls", "Colony Of Ants", "Business Of Ferrets", "Crash Of Hippopotami",
	   "An abominable sight of monks", "Troop Of Horses", "Leash Of Deer", "Skein Of Geese (In Flight)",
	   "A shiver of sharks", "A nucleus of physicists", "Sedge Of Herons", "Gang Of Elk", "Swarm Of Gnats",
	   "Shoal Of Herrings", "Group Of Guinea Pigs", "Flush Of Ducks", "Cloud Of Gnats", "Parcel Of Deer",
	   "Herd Of Goats", "Tribe Of Baboons", "An unhappiness of husbands", "Trip Of Goats", "Sleuth Of Bears",
	   "An exaltation of larks", "Army Of Ants", "Storytelling Of Crows", "Aerie Of Hawks", "A grope of groupies",
	   "Swarm Of Ants", "A lechery of priests", "Tribe Of Goats", "An enterance of actresses", "Wing Of Dragons",
	   "Pack Of Grouse", "Leash Of Foxes", "Swarm Of Bees", "A rhumba of rattlesnakes", "A helix of geneticists",
	   "Harras Of Horses", "Swarm Of Butterflies", "A shower of meteorologists", "An ambush of tigers",
	   "Paddling Of Ducks", "Clutter Of Cats", "A crossing of zebras", "Fesnyng Of Ferrets", "Litter Of Dogs (Puppies)",
	   "Leash Of Hares", "A fagot of drummers", "Flock Of Camels", "A murder of crows", "Pack Of Bears (Polar Bears)",
	   "Drove Of Hares", "Siege Of Herons", "Kennel Of Dogs", "Herd Of Boar", "Bury Of Conies", "Flock Of Geese",
	   "Pace Of Donkeys", "Bed Of Clams", "Cover Of Coots", "Hedge Of Herons", "Cete Of Badgers", "Team Of Ducks",
	   "Herd Of Donkeys", "Yoke Of Cattle (Two)", "Prickle Of Hedgehogs", "Herd Of Chinchillas",
	   "Litter Of Cats (Kittens)", "A sprig of vegatarians", "Weyr Of Dragons", "A sodom of shepherds", "Rag Of Colts",
	   "Rabble Of Butterflies", "Trace Of Hares", "Band Of Coyotes", "Flight Of Birds", "Run Of Fish",
	   "Destruction Of Cats (Wild Cats)", "Herd Of Deer", "Brood Of Chickens", "Dissimulation Of Birds",
	   "Grist Of Bees", "Brood Of Chicks", "Bevy Of Doves", "Colony Of Beavers", "Brace Of Ducks",
	   "A tough of lesbians", "Herd Of Horses", "Team Of Cattle", "Herd Of Hippopotami", "Memory Of Elephants",
	   "A phalanx of umbrellas", "Flock Of Birds", "Kindle Of Cats (Kittens)", "An unkindness of ravens",
	   "Wake Of Buzzards", "Flock Of Ducks", "Pounce Of Cats", "A hack of smokers", "Convocation Of Eagles",
	   "Corps Of Giraffes", "Colony Of Gulls", "Lead Of Foxes", "Sounder Of Boar", "Congress Of Baboons",
	   "Hive Of Bees", "Raft Of Ducks", "Peep Of Chickens", "Brood Of Hens", "Herd Of Cattle", "Flight Of Dragons",
	   "Bloat Of Hippopotami", "Siege Of Bitterns", "Singular Of Boar", "Murder Of Crows", "Cast Of Hawks",
	   "Mob Of Emus", "A peck of Frenchmen", "Cartload Of Chimpanzees", "Congregation Of Crocodiles", "Kettle Of Hawks",
	   "Herd Of Elk", "Herd Of Giraffes", "Clowder Of Cats", "Parade Of Elephants", "Drove Of Donkeys", "Dole Of Doves",
	   "Rake Of Colts", "Herd Of Buffalo", "Stable Of Horses", "Horde Of Hamsters", "Array Of Hedgehogs",
	   "Husk Of Hares", "Sedge Of Cranes", "Clutch Of Chicks", "Volery Of Birds", "Flight Of Bees", "Swarm Of Eels",
	   "Siege Of Cranes", "Herd Of Gnus", "Gaggle Of Geese", "Flight Of Cormorants", "Shoal Of Fish",
	   "Nuisance Of Cats (House Cats)", "Herd Of Chamois", "Kine Of Cattle", "Knot Of Frogs", "Charm Of Goldfinches",
	   "Congregation Of Birds", "Warren Of Hares", "Chattering Of Chicks", "Catch Of Fish", "Culture Of Bacteria",
	   "Cast Of Ferrets", "Drove Of Goats", "Pod Of Dolphins", "A culture of bacteria", "Kendle Of Cats (Kittens)",
	   "Lodge Of Beavers", "Nest Of Hornets", "Chain Of Bobolinks", "Quiver Of Cobras", "Flight Of Doves",
	   "Drift Of Hogs", "Horde Of Gerbils", "A flock of tourists", "Skulk Of Foxes", "Leash Of Greyhounds",
	   "Haul Of Fish", "Sloth Of Bears", "A beautification of spatulas", "Sedge Of Bitterns", "Swarm Of Flies",
	   "Clash Of Bucks", "Trip Of Hares", "Glaring Of Cats", "Pack Of Dogs", "Covey Of Grouse", "A galaxy of beauties",
	   "Aerie Of Eagles", "A metamorphosis of ovoids", "Dout Of Cats (House Cats)", "Dule Of Doves", "Drove Of Cattle",
	   "A goring of butchers", "Team Of Horses", "A souffle of clouds", "Float Of Crocodiles", "Band Of Gorillas",
	   "Trip Of Dotterel", "Wedge Of Geese (Flying In A 'V')", "Glint Of Goldfish", "Parcel Of Hogs", "Colony Of Frogs",
	   "Brace Of Bucks", "School Of Fish", "Army Of Frogs"]
jokes = ["Just recently ended a 5 year relationship. It's OK though, it wasn’t my relationship.",
		 "Yo mama is like a bowling ball. She gets picked up, fingered, thrown away, and she keeps coming back for more!",
		 "Went to the barbers today and asked to get my hair cut like Justin Bieber. He totally shaved my head bald. I said 'What the hell have you done. Justin Bieber doesn't have his hair cut like this!!', the barber said 'He would if he came into my shop.'",
		 "Just named my new kid cancer. That way when people hear about me beating cancer it'll make me sound better.",
		 "Have you heard about the new aftershave the Catholic Church have just released?", "It's called 'Eau My God'.",
		 "I used to work as a mechanic fixing jet-ski engines at my local Sea World Center but I got fired after blowing a seal.",
		 "Don't you just hate it when your Korean grandma makes a really nice chow-mein but then you find out your dogs gone missing.",
		 "I wish I were a unicorn…. so I could stab idiots with my head.",
		 "Had a great time watching Fifty Shades Of Grey at the cinema with my girlfriend. The film was terrible but the reaction of the people sitting in front of us after I flicked mayonnaise on them was hilarious.",
		 "If Steve has 20 dollars and Tyrone takes 16, what color is Tyrone?",
		 "Two years ago I asked the girl of my dreams on a date, today I asked her to marry me. She said no, on both occasions.",
		 "Recently had a great money saving idea. Instead of paying for teeth whitening I've decided to get a sun-tan instead. ",
		 "I used to be a gynecologist but I had to quit due to health reasons. I kept getting tunnel vision.",
		 "Got a valentines card from my Grandma earlier today which was sweet but unnecessary, we haven't had sex in years.",
		 "People always ask me why I'm single. I'm single by choice… unfortunately it's not my choice",
		 "Have you heard about this new thing you can have that transfers the thoughts and memories of one person to another person. It's called a CONVERSATION.",
		 "Yo mama is so harry big foot took a picture of her.",
		 "Just been sacked from my job at the casino. Apparently when they hired me as a dealer I wasn't supposed to try and sell crack cocaine to customers.",
		 "Did you hear about the Irish metal detector enthusiast who dug a hole 70ft deep? It turns out he had steel toecap shoes on."]
localtime = time.localtime(time.time())
d = datetime.date.today()
ftime = "[%s]" % (d.strftime('%H:%M:%S'))
raw_text = ''
rawer_text = ''
user = raw_text[1:raw_text.find('!')]
msg = raw_text[raw_text.find(':'):500][1:500]
msg = msg[msg.find(':'):500][1:500].replace('\n', '').replace('\r', '')
line = ''
msgs = ''
notice = False
rec = ''
pm = False
google_api="AIzaSyDkxx5jT2ZWsLZH6vQ_PctkqLngUarvfbc"
torrent_hash = ''

def check_operator():
	operators = config.operator.replace(', ', ',').replace(' ', '').split(',')
	operatorlist = ['']
	for item in operators:
		operatorlist.append(item.lower())
	if user.lower() in operatorlist:
		return True
	else:
		return False


def check_ignorelist():
	if lists.ignorelist == '':
		return False
	#ignorelist = lists.ignorelist.replace(', ', ',').replace(' ', '').split(',')
	ignorelist = lists.ignorelist
	ilist = []
	for item in ignorelist:
		ilist.append(item.lower())
	if user.lower() in ilist:
		return True
	else:
		return False

def reload_lists():
	lists = reload(lists)
def check_whitelist():
	#if lists.whitelist == '':
	#    return False
	#whitelist = lists.whitelist.replace(', ', ',').replace(' ', '').split(',')
	whitelist = lists.whitelist
	wlist = []
	for item in whitelist:
		wlist.append(item.lower())
	if user.lower() in wlist:
		return True
	else:
		return False


def append_whitelist(name):
	whitelist = lists.whitelist.replace(', ', ',').replace(' ', '').split(',')
	ignorelist = lists.ignorelist.replace(', ', ',').replace(' ', '').split(',')
	whitelist.append(name)
	f = open('lists.py', 'w')
	f.write('whitelist = "%s"\n' % whitelist.split(','))
	f.write('ignorelist = "%s"\n' % ignorelist.split(','))
	f.close()
	lists = reload(lists)


def append_ignorelist(name):
	whitelist = lists.whitelist.replace(', ', ',').replace(' ', '').split(',')
	ignorelist = lists.ignorelist.replace(', ', ',').replace(' ', '').split(',')
	whitelist.append(name)
	f = open('lists.py', 'w')
	f.write('whitelist = "%s"\n' % whitelist.split(','))
	f.write('ignorelist = "%s"\n' % ignorelist.split(','))
	f.close()
	lists = reload(lists)


def ssend(text):
	if config.verbose == True:
		print ftime + ' >> ' + text
	s.send(text + '\n')


def csend(text):
	if notice == True:
		if config.verbose == True:
			print ftime + ' >> ' + 'NOTICE %s :%s' % (config.channel, text)
		else:
			print ftime + ' >> NOTICE %s: %s' % (config.channel, text)
		s.send('NOTICE %s :%s%s' % (rec, ceq.hiddenc.encode('utf-8'), text) + '\n')
		return
	if pm == True:
		if config.verbose == True:
			print ftime + ' >> ' + 'PRIVMSG %s :%s' % (config.channel, text)
		else:
			print ftime + ' >> PM %s: %s' % (config.channel, text)
		s.send('PRIVMSG %s :%s%s' % (rec, ceq.hiddenc.encode('utf-8'), text) + '\n')
		return
	if config.verbose == True:
		print ftime + ' >> ' + 'PRIVMSG %s :%s' % (config.channel, text)
	else:
		print ftime + ' >> %s: %s' % (config.channel, text)
	s.send('PRIVMSG %s :%s%s' % (config.channel, ceq.hiddenc.encode('utf-8'), text) + '\n')


def psend(user, text):
	if config.verbose == True:
		print ftime + ' >> ' + "PRIVMSG %s :%s" % (user, text)
	else:
		print ftime + ' >> %s: %s' % (user, text)
	s.send("PRIVMSG %s :%s\n" % (user, text))

