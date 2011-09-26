from .. import bot, auth, json

plusses = {}

try:
	with open('plus.db') as f:
		plusses = json.load(f)
except IOError:
	pass

@bot.register(r'\+1 (.*)')
@auth.required
def plus_one(bot, linedata, authed, matches):
	if authed:
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

@bot.register_atexit
def save_json(bot):
	with open('plus.db', 'w') as f:
		json.dump(plusses, f)
