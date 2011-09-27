from .. import bot

import time

last = {}

@bot.preregister()
def log_last(bot, linedata, match):
	last[linedata.sender] = (time.gmtime(), linedata.line)

@bot.register("[Ww]at zei (.*)\??")
def log_last(bot, linedata, matches):
	s = matches[0]
	if s in last:
		bot.reply("[%s] <%s> %s" % (time.strftime('%H:%M:%S', last[s][0]), s, last[s][1]), linedata)
