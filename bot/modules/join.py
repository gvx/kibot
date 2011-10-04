from .. import bot, auth

@bot.register("join (.*)")
@auth.admin
@auth.required
def reload_(bot, linedata, matches):
	bot.join(matches[0])

@bot.register("part (.*)")
@auth.admin
@auth.required
def reload_(bot, linedata, matches):
	bot.part(matches[0])
