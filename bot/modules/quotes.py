from .. import bot, auth, persist

import random

quotes = persist('quotes.db')
log = {}

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
	else: #quote search
		s = matches[0].lower()
		for k, quotelist in quotes.iteritems():
			for quote in quotelist:
				if s in quote.lower():
					bot.reply('<' + k + '> ' + quote, linedata)
