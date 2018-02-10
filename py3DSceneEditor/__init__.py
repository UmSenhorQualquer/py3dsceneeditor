__version__     = "0.1"
__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "Attribution-NonCommercial-ShareAlike 4.0 International"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"

import loggingbootstrap; 
from   importlib.util import find_spec

from pysettings import conf; conf += 'py3DSceneEditor.settings'

####################################################
## Load the user settings in case the file exists ##
####################################################
try:
	import user_settings; conf += user_settings
except:
	pass
####################################################
####################################################

# CHECK IF PYFORMS IS AVAILABLE WITHOUT ACTUALLY IMPORTING IT
pyforms_spec = find_spec("pyforms")
if not pyforms_spec: exit("Could not load pyforms! Is it installed?")



print('LEVEL', conf.PYFORMS_LOG_HANDLER_CONSOLE_LEVEL)

loggingbootstrap.create_double_logger("py3DSceneEditor", conf.PY3DEDITOR_LOG_HANDLER_CONSOLE_LEVEL, conf.PY3DEDITOR_LOG_FILENAME , conf.PY3DEDITOR_LOG_HANDLER_FILE_LEVEL)
loggingbootstrap.create_double_logger("pyforms", 		 conf.PYFORMS_LOG_HANDLER_CONSOLE_LEVEL,    conf.PYFORMS_LOG_FILENAME,     conf.PYFORMS_LOG_HANDLER_FILE_LEVEL)
