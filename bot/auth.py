from functools import wraps

class Auth(object):
	def __init__(self, bot):
		self.bot = bot
		self.bot.register_notice(self.receive_notice)
		self.callbacks = []
	def check(self, nick):
		self.bot.say("info " + nick, to="NickServ")
	def receive_notice(self, bot, linedata):
		if linedata.line.endswith('is not registered.'):
			self.callbacks.pop(0)(False)
		elif linedata.line.startswith("Last seen"):
			self.callbacks.pop(0)("now" in linedata.line)
	def required(self, f):
		@wraps(f)
		def wrapper(bot, linedata, *args):
			self.check(linedata.sender)
			self.callbacks.append(lambda x: f(bot, linedata, x, *args))
		return wrapper
