
import logging

from logging import info as info
from logging import warning as warning
from logging import error as error
from logging import debug as debug

from .config import ConfigLogging

def setup(conf: ConfigLogging) -> bool:

    if conf.level == 0:
        level = 20 # Info Logging
    elif conf.level == 1:
        level = 30 # Warn Logging
    elif conf.level == 2:
        level = 40 # Error Logging
    elif conf.level == 3:
        level = 50 # Critical Logging
    else:
        level = 10 # Debug Logging

    try:
        if conf.syslog == False:
            logging.basicConfig(filename=conf.file,
                filemode='a',
                format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                datefmt='%b %d %H:%M:%S',
                level=level
            )
    except Exception as err:
        print(err)
        return False
    
    return True
# // setup(conf: ConfigLogging) -> bool

"""
conf = ConfigLogging()
conf.file = "test.log"
conf.syslog = False
conf.level = 3
setup(conf)

info("Nachricht 1")
warning("Nachricht 2")
error("Nachricht 3")
debug("Nachricht 4")
"""