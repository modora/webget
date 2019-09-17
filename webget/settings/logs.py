from pathlib import Path

from webget import app_data

##################### SETTINGS ###########################
# Link for logging settings
# http://doc.scrapy.org/en/latest/topics/logging.html#logging-settings
LOG_ENABLED = True
LOG_STDOUT = True
LOG_FILE = Path(app_data, 'logs', 'scrapy.log')

################### POST-PROCESSING #####################

if LOG_FILE:
	LOG_FILE = Path(LOG_FILE)
	LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
	LOG_FILE.touch(exist_ok=True)