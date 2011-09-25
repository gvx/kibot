from bot import Bot
from auth import Auth

import json

bot = Bot('Kibot')
auth = Auth()

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

