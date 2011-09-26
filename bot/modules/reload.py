from .. import bot, auth, reload_modules

@bot.register("reload")
@auth.required
def reload_(bot, linedata, match):
	print "reloading"
	reload_modules()
