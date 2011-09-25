from .. import bot

try:
	with open('pwd.db') as f:
		passwd = f.read().rstrip()
except IOError:
	passwd = None

if passwd:
	@bot.register_connects
	def do_login(bot):
		bot.say('identify ' + passwd, to='NickServ')
