#from .wiki import *
#from .quotes import *
#from .plus import *

from glob import iglob
from os.path import dirname, join, splitext, basename

#import all modules
module_list = [splitext(basename(x))[0] for x in iglob(join(dirname(__file__), '*.py'))]

for name in module_list:
	__import__('bot.modules.' + name, globals(), locals(), [], -1)

del iglob, dirname, join, splitext, basename
