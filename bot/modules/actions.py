from .. import bot

@bot.register("\x01ACTION .*" + bot.name + ".*\x01")
def action(bot, linedata, match):
	bot.reply(match.replace(bot.name, linedata.sender), linedata)
