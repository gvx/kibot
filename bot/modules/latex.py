from .. import bot

import urllib

latexurl = 'http://latex.codecogs.com/svg.latex?'

@bot.register(r'\$(.*?)\$', multi=True)
def latex(bot, linedata, matches):
	for match in matches:
		bot.reply(latexurl + urllib.quote(match), linedata)

lines = {}

@bot.register('<latex>(.*)')
def latex_multi_line_open(bot, linedata, matches):
	lines[linedata.sender] = [matches[0]]
	return True

@bot.register('(.*)</latex>')
def latex_multi_line_close(bot, linedata, matches):
	s = linedata.sender
	if s in lines:
		lines[s].append(matches[0])
		bot.reply(latexurl + urllib.quote(' '.join(lines[s])), linedata)
		del lines[s]
	return True


@bot.register('.*')
def latex_multi_line_middle(bot, linedata, matches):
	s = linedata.sender
	if s in lines:
		lines[s].append(matches)
