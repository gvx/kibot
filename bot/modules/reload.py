from .. import bot, auth, reload_modules

@bot.register("reload (.*)")
def reload_(bot, linedata, match):
	print "reloading"
	if match[0] == bot.name:
		reload_modules()
