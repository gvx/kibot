from .. import bot, auth, json

class WikiEntry(object):
	def __init__(self, author, text):
		self.author = author
		self.text = text
	def modify(self, author, text):
		if author == self.author:
			self.text = text

wiki = {}

try:
	with open('wiki.db') as f:
		w = json.load(f)
		for k in w:
			wiki[k] = WikiEntry(*w[k])
except IOError:
	pass

@bot.register(r'\[\[(.*)\]\]:=(.*)')
@auth.required
def define_wiki(bot, linedata, matches):
	name, text = matches
	if name in wiki:
		wiki[name].modify(linedata.sender, text)
	else:
		wiki[name] = WikiEntry(linedata.sender, text)

@bot.register(r'\[\[(.*?)\]\]', multi=True)
def show_wiki(bot, linedata, matches):
	if "]]:=" not in linedata.line:
		for match in matches:
			if match in wiki:
				bot.reply(wiki[match].text, linedata)

@bot.register_atexit
def save_json(bot):
	with open('wiki.db', 'w') as f:
		w = {}
		for k in wiki:
			w[k] = (wiki[k].author, wiki[k].text)
		json.dump(w, f)
