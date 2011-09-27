from bot import Bot
from auth import Auth

bot = Bot('Kibot')
auth = Auth(bot)

from persist import persist, json

def reload_modules():
	for f in bot.quit_regs:
		f(bot)
	bot.clear_rules()

	import sys
	for mod in sys.modules.keys():
		if mod.startswith('bot.modules.'):
			del sys.modules[mod]

	reload(modules)

from . import modules

