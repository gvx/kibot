from .. import bot

import time

last = {}

@bot.preregister()
def log_last(bot, linedata, match):
	if linedata.receiver != bot.name:
		last[linedata.sender] = (time.localtime(), linedata.line)

@bot.register(r"[Ww]at zei (.*?)\??$")
def log_last(bot, linedata, matches):
	s = matches[0]
	if s in last:
		bot.reply("[%s] <%s> %s" % (time.strftime('%H:%M:%S', last[s][0]), s, last[s][1]), linedata)
