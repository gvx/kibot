from .. import bot

@bot.register(r'<(/?)3 (.*)')
def love_hate(bot, linedata, matches):
	lh = matches[0]
	s = matches[1].strip()
	if s.title() == bot.name:
		s = linedata.sender
	bot.reply('<'+lh+'3 ' + s, linedata)

