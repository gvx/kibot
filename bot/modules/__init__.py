#from .wiki import *
#from .quotes import *
#from .plus import *

from glob import iglob
from os.path import dirname, join, splitext, basename

#import all modules
module_list = [splitext(basename(x))[0] for x in iglob(join(dirname(__file__), '*.py'))]
__all__ = module_list + ['reload_modules']

def reload_modules():
	pass #FIXME

del iglob, dirname, join, splitext, basename
