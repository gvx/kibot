from .. import bot, auth, reload_modules

@bot.register("reload")
@auth.required
def reload_(bot, linedata, authed, match):
	if authed:
		print "reloading"
		reload_modules()
