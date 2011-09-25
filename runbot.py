from bot import bot
import time

bot.connect('irc.ai.ru.nl', 6667)
time.sleep(2)
bot.join('#kiru')
bot.wait()

