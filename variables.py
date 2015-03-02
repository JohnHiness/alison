#!/usr/bin/python
import socket
import sys
import random
import time
import datetime
import config
import soconnect

version = "0.16.4"
s = soconnect.s
leave_messages = ["I will be blac.. cough cough ..back. I'll be back.", "SOMEONES HACKING! I'M OFF TO BATTLE!", "I can fix everything. I have duct tape.", "Can't think of a joke. Ask Cortana.", "Pooooooooofffffff i'm outta here..", "I generally avoid temptation.. unless I can't resist it"]
hva = ["Piteousness Of Doves", "A charm of finches", "Skein Of Goslings", "Army Of Caterpillars", "Herd Of Antelope", "A mischief of mice", "Implausibility Of Gnus", "Cote Of Doves", "Bevy Of Deer (Roe Deer)", "Shrewdness Of Apes", "A flange of baboons", "Flock Of Chickens", "Horde Of Gnats", "Down Of Hares", "Colony Of Badgers", "Herd Of Elephants", "Flange Of Baboons", "Passel Of Hogs", "Tower Of Giraffes", "Charm Of Finches", "A parliament of owls", "Colony Of Ants", "Business Of Ferrets", "Crash Of Hippopotami", "An abominable sight of monks", "Troop Of Horses", "Leash Of Deer", "Skein Of Geese (In Flight)", "A shiver of sharks", "A nucleus of physicists", "Sedge Of Herons", "Gang Of Elk", "Swarm Of Gnats", "Shoal Of Herrings", "Group Of Guinea Pigs", "Flush Of Ducks", "Cloud Of Gnats", "Parcel Of Deer", "Herd Of Goats", "Tribe Of Baboons", "An unhappiness of husbands", "Trip Of Goats", "Sleuth Of Bears", "An exaltation of larks", "Army Of Ants", "Storytelling Of Crows", "Aerie Of Hawks", "A grope of groupies", "Swarm Of Ants", "A lechery of priests", "Tribe Of Goats", "An enterance of actresses", "Wing Of Dragons", "Pack Of Grouse", "Leash Of Foxes", "Swarm Of Bees", "A rhumba of rattlesnakes", "A helix of geneticists", "Harras Of Horses", "Swarm Of Butterflies", "A shower of meteorologists", "An ambush of tigers", "Paddling Of Ducks", "Clutter Of Cats", "A crossing of zebras", "Fesnyng Of Ferrets", "Litter Of Dogs (Puppies)", "Leash Of Hares", "A fagot of drummers", "Flock Of Camels", "A murder of crows", "Pack Of Bears (Polar Bears)", "Drove Of Hares", "Siege Of Herons", "Kennel Of Dogs", "Herd Of Boar", "Bury Of Conies", "Flock Of Geese", "Pace Of Donkeys", "Bed Of Clams", "Cover Of Coots", "Hedge Of Herons", "Cete Of Badgers", "Team Of Ducks", "Herd Of Donkeys", "Yoke Of Cattle (Two)", "Prickle Of Hedgehogs", "Herd Of Chinchillas", "Litter Of Cats (Kittens)", "A sprig of vegatarians", "Weyr Of Dragons", "A sodom of shepherds", "Rag Of Colts", "Rabble Of Butterflies", "Trace Of Hares", "Band Of Coyotes", "Flight Of Birds", "Run Of Fish", "Destruction Of Cats (Wild Cats)", "Herd Of Deer", "Brood Of Chickens", "Dissimulation Of Birds", "Grist Of Bees", "Brood Of Chicks", "Bevy Of Doves", "Colony Of Beavers", "Brace Of Ducks", "A tough of lesbians", "Herd Of Horses", "Team Of Cattle", "Herd Of Hippopotami", "Memory Of Elephants", "A phalanx of umbrellas", "Flock Of Birds", "Kindle Of Cats (Kittens)", "An unkindness of ravens", "Wake Of Buzzards", "Flock Of Ducks", "Pounce Of Cats", "A hack of smokers", "Convocation Of Eagles", "Corps Of Giraffes", "Colony Of Gulls", "Lead Of Foxes", "Sounder Of Boar", "Congress Of Baboons", "Hive Of Bees", "Raft Of Ducks", "Peep Of Chickens", "Brood Of Hens", "Herd Of Cattle", "Flight Of Dragons", "Bloat Of Hippopotami", "Siege Of Bitterns", "Singular Of Boar", "Murder Of Crows", "Cast Of Hawks", "Mob Of Emus", "A peck of Frenchmen", "Cartload Of Chimpanzees", "Congregation Of Crocodiles", "Kettle Of Hawks", "Herd Of Elk", "Herd Of Giraffes", "Clowder Of Cats", "Parade Of Elephants", "Drove Of Donkeys", "Dole Of Doves", "Rake Of Colts", "Herd Of Buffalo", "Stable Of Horses", "Horde Of Hamsters", "Array Of Hedgehogs", "Husk Of Hares", "Sedge Of Cranes", "Clutch Of Chicks", "Volery Of Birds", "Flight Of Bees", "Swarm Of Eels", "Siege Of Cranes", "Herd Of Gnus", "Gaggle Of Geese", "Flight Of Cormorants", "Shoal Of Fish", "Nuisance Of Cats (House Cats)", "Herd Of Chamois", "Kine Of Cattle", "Knot Of Frogs", "Charm Of Goldfinches", "Congregation Of Birds", "Warren Of Hares", "Chattering Of Chicks", "Catch Of Fish", "Culture Of Bacteria", "Cast Of Ferrets", "Drove Of Goats", "Pod Of Dolphins", "A culture of bacteria", "Kendle Of Cats (Kittens)", "Lodge Of Beavers", "Nest Of Hornets", "Chain Of Bobolinks", "Quiver Of Cobras", "Flight Of Doves", "Drift Of Hogs", "Horde Of Gerbils", "A flock of tourists", "Skulk Of Foxes", "Leash Of Greyhounds", "Haul Of Fish", "Sloth Of Bears", "A beautification of spatulas", "Sedge Of Bitterns", "Swarm Of Flies", "Clash Of Bucks", "Trip Of Hares", "Glaring Of Cats", "Pack Of Dogs", "Covey Of Grouse", "A galaxy of beauties", "Aerie Of Eagles", "A metamorphosis of ovoids", "Dout Of Cats (House Cats)", "Dule Of Doves", "Drove Of Cattle", "A goring of butchers", "Team Of Horses", "A souffle of clouds", "Float Of Crocodiles", "Band Of Gorillas", "Trip Of Dotterel", "Wedge Of Geese (Flying In A 'V')", "Glint Of Goldfish", "Parcel Of Hogs", "Colony Of Frogs", "Brace Of Bucks", "School Of Fish", "Army Of Frogs"]
localtime = time.localtime(time.time())
d = datetime.date.today()
ftime = "[%s]" % (d.strftime('%H:%M:%S'))
raw_text = ''
rawer_text = ''
user = raw_text[1:raw_text.find('!')]
msg = raw_text[raw_text.find(':'):500][1:500]
msg = msg[msg.find(':'):500][1:500].replace('\n', '').replace('\r', '')


def check_admin():
	admins = config.admin.replace(', ', ',').replace(' ', ' ').split(',')
	adminlist = ['']
	for item in admins:
		adminlist.append(item.lower())
	if user.lower() in adminlist:
		return True
	else:
		return False
def ssend(text):
	if config.verbose == True:
	        print ftime + ' >> ' + text + '\n'	
        s.send(text + '\n')
def csend(text):
	if config.verbose == True:
		print ftime + ' >> ' + 'PRIVMSG %s :%s\n' % (config.channel, text)
	else:
	        print ftime + ' >> %s: %s' % (config.channel, text)
        s.send('PRIVMSG %s :%s\n' % (config.channel, text))
def psend(user, text):
	if config.verbose == True:
		print ftime + ' >> ' + "PRIVMSG %s :%s\n" % (user, text)
	else:
	        print ftime + ' >> %s: %s' % (user, text)
        s.send("PRIVMSG %s :%s\n" % (user, text))

