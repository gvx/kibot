from .. import bot

import urllib

@bot.register(r'\$(.*?)\$', multi=True)
def latex(bot, linedata, matches):
	for match in matches:
		bot.reply('http://latex.codecogs.com/svg.latex?' + urllib.quote(match), linedata)
