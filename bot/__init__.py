from bot import Bot
from auth import Auth

import json

bot = Bot('Kibot')
auth = Auth()

def reload_modules():
	for f in bot.quit_regs:
		f(bot)
	bot.clear_rules()

	reload(modules)

from . import modules

