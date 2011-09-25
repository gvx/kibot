from .. import bot, auth, reload_modules

@bot.register("reload (.*)")
def reload_(bot, linedata, match):
	if match[0] == bot.name:
		print "reloading"
		reload_modules()
