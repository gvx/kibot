from . import bot

import json

def persist(filename, default=None):
	try:
		with open(filename) as f:
			w = json.load(f)
	except IOError:
		w = default if default is not None else {}

	@bot.register_atexit
	def save_json(bot):
		with open(filename, 'w') as f:
			json.dump(w, f)

	return w
