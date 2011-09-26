from .. import bot, auth, json

import random

quotes = {}
log = {}

try:
	with open('quotes.db') as f:
		quotes = json.load(f)
except IOError:
	pass

@bot.preregister('.*')
def log_data(bot, linedata, match):
	s = linedata.sender
	if s not in log:
		log[s] = []
	log[s].append(linedata.line.strip())
	if len(log[s]) > 10:
		log[s].pop(0)

@bot.register(r'\+Q <(.*?)> (.*)')
@auth.required
def add_quote(bot, linedata, matches):
	m = matches[1].strip()
	s = matches[0].title()
	if s in log and m in log[s]:
		if s not in quotes:
			quotes[s] = []
		quotes[s].append(m)

@bot.register(r'\?Q (.*)')
def show_quote(bot, linedata, matches):
	s = matches[0].title()
	if s in quotes:
		bot.reply('<' + matches[0] + '> ' + random.choice(quotes[s]), linedata)

@bot.register_atexit
def save_json(bot):
	with open('quotes.db', 'w') as f:
		json.dump(quotes, f)
