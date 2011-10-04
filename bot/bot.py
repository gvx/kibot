import socket
import re

class LineData(object):
	def __init__(self, line):
		self.sender, self.receiver, self.line, self.action = self.extract_data(line)
	def extract_data(self, line):
		frags = line.strip().split(' ', 3)
		if frags:
			if frags[1] == 'QUIT':
				return frags[0][1:].split('!',1)[0].title(), '*', len(frags) > 3 and frags[2] + ' ' + frags[3] or frags[2], frags[1]
			return frags[0][1:].split('!',1)[0].title(), frags[2].title(), len(frags) > 3 and frags[3][1:] or '', frags[1]
		else:
			return '', '', '', ''

class Bot(object):
	def __init__(self, name='aibot'):
		self.name = name
		self.clear_rules()
		self.has_quit = False
	def clear_rules(self):
		self.rules = []
		self.quit_regs = []
		self.join_regs = []
		self.connect_regs = []
		self.users = {}
		self.regs = {'JOIN': [], 'PART': [], 'QUIT': [], 'NOTICE': []}
	def connect(self, server, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((server, port))
		print(self.socket.recv(4096))
		self.send('NICK', self.name)
		self.send('USER', self.name, self.name, self.name, ':Kibot Junior')
	def join(self, channel):
		print 'JOIN |', channel, '<-', self.name
		self.send('JOIN', channel)
	def part(self, channel):
		print 'PART |', channel, '<-', self.name
		self.send('PART', channel)
	def reply(self, msg, linedata):
		if linedata.receiver == self.name:
			self.say(msg, linedata.sender)
		else:
			self.say(msg, linedata.receiver)
	def say(self, msg, to):
		print 'PRIVMSG |', to, '<-', self.name, ':', msg
		self.send('PRIVMSG', to, ':'+msg)
	def send(self, *msg):
		self.socket.send(' '.join(msg)+'\r\n')
	def quit(self):
		self.send('QUIT')
		#self.has_quit = True
		for f in self.quit_regs:
			f(self)
	def wait(self):
		for f in self.connect_regs:
			f(self)
		try:
			while not self.has_quit:
				self.act()
		finally:
			self.quit()
	def act(self):
		data = ''
		while not data.endswith('\r\n'):
			data += self.socket.recv(4096)
		if 'PING' in data:
			self.send('PONG', data.split()[1])
			return
		#try:
		self.receive(data.strip())
		#except Exception as e:
		#	self.say(str(e))
	@staticmethod
	def match(rule, text):
		r = re.match(rule, text)
		if r:
			return r.groups() or r.group(0)
	def receive(self, text):
		for line in text.split('\r\n'):
			self.receive_line(line)
	def receive_line(self, text):
		linedata = LineData(text)
		print linedata.action, '|', linedata.sender, '->', linedata.receiver, ':', linedata.line
		if linedata.line and linedata.action == 'PRIVMSG':
			for f, rule, multi in self.rules:
				match = rule is None or (multi and re.findall or Bot.match)(rule, linedata.line)
				if match:
					if f(self, linedata, match):
						break
		elif linedata.action in self.regs:
			for f in self.regs[linedata.action]:
				f(self, linedata)
		elif linedata.action == '353':
			channel, names = linedata.line.lstrip().split(':', 1)
			if channel not in self.users:
				self.users[channel] = []
			self.users[channel].extend(name.lstrip('@') for name in names.split())
		elif linedata.action == '366':
			channel = '#' + linedata.line.lstrip().split(':', 1)[0]
			if channel in self.users:
				users = self.users[channel]
				del self.users[channel]
			else:
				users = []
			for f in self.join_regs:
				f(self, channel, users)
	def preregister(self, rule=None, multi=False):
		def k(f):
			self.rules.insert(0, (f, rule, multi))
			return f
		return k
	def register(self, rule=None, multi=False):
		def k(f):
			self.rules.append((f, rule, multi))
			return f
		return k
	def register_atexit(self, f):
		self.quit_regs.append(f)
		return f
	def register_join(self, f):
		self.regs['JOIN'].append(f)
		return f
	def register_part(self, f):
		self.regs['PART'].append(f)
		return f
	def register_quit(self, f):
		self.regs['QUIT'].append(f)
		return f
	def register_notice(self, f):
		self.regs['NOTICE'].append(f)
		return f
	def register_joinschannel(self, f):
		self.join_regs.append(f)
		return f
	def register_connects(self, f):
		self.connect_regs.append(f)
		return f
