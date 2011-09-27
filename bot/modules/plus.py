from .. import bot, auth, persist

plusses = persist('plus.db')

@bot.register(r'\+1 (.*)')
@auth.required
def plus_one(bot, linedata, matches):
	s = matches[0]
	if s != linedata.sender:
		if s not in plusses:
			plusses[s] = 1
		else:
			plusses[s] += 1

@bot.register(r'hoeveel punten (.*)')
def plus_what(bot, linedata, matches):
	s = matches[0]
	bot.reply(str(plusses.get(s, 0)), linedata)
