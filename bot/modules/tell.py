from .. import bot, auth, persist

messages = persist('messages.db')

@bot.preregister(".*")
@bot.register_join
def do_tell(bot, linedata, match=None):
	s = linedata.sender
	if s in messages:
		for sender, private, message in messages[s]:
			if private:
				bot.say(sender + " zei " + message, to=s)
			else:
				bot.reply(s + ": " + sender + " zei " + message, linedata)
		del messages[s]

@bot.register("[Zz]eg (.*?) (.*)")
@auth.required
def add_tell(bot, linedata, matches):
	r = matches[0].title()
	msg = matches[1]
	s = linedata.sender
	private = linedata.receiver.title() == bot.name.title()
	if r not in messages:
		messages[r] = []
	messages[r].append((s, private, msg))
